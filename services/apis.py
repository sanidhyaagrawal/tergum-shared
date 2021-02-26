
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import auth
from common.models import Rate

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from services.models import Job, JobType, Contract
from common.models import Attachment
from rest_framework import status
import re
import services.serializers as serializers

#function to create file name based on text
from services.verifiers import create_file_name

#As end user might want to go back to step-1, add/remove some files and then again 
#continue to the next step which is not possible with csrf velidation
#we have to exempt csrf validation for these perticular apis in order to achive this functionality.
from core.authenticators import CsrfExemptSessionAuthentication

@api_view(['POST', 'DELETE'])
@throttle_classes([AnonRateThrottle]) #Limiting number of API calls a user can make.
@authentication_classes([CsrfExemptSessionAuthentication, SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated]) #requires the request user to be authenticated
def attchment_api(request, attachment_id=None): 
    '''
    add an attachment to a Job
    '''
    ISO = request.LANGUAGE_CODE
    if request.method == 'POST': #api/attchment_api
        data = request.data
        job_id = data.get('job_id')
        attachment = data.get('attachment')
        text_input = data.get('text_input')
        
        #get Job object from databse for the job_id
        job_obj = Job.objects.get(job_id=job_id)

        #word count for text area input
        input_word_count = 0
        lines_in_text_input = text_input.split('\n')
        for lines in lines_in_text_input:
            first, _, rest = lines.partition('[[[')
            _, _, rest = rest.partition(']]]')
            line = ' '.join([first.strip(), rest.strip()])            
            input_word_count += len(line.split())

        hasText = False #flag for if user has input text in textarea
        hasFile = False #flag for if user has uploaded a file.


        from django.core.files.base import ContentFile
        import datetime
        input_text_file_name = "{}.txt".format(datetime.datetime.now()) #placeholder name if we are unable to create one from the input text
        if input_word_count > 0:
            #if user has input text in textarea, then create a .txt file form user's input    
            hasText = True    

            #craete a file name based on input text
            input_text_file_name = create_file_name(lines_in_text_input)
            
            #create and add attachment to the Job
            attachment_obj = Attachment.objects.create(owner=request.user, word_count=input_word_count, orignal_filename=input_text_file_name)    
            encoded_text = text_input.encode('utf-8', 'replace')
            print(encoded_text)
            attachment_obj.file.save(input_text_file_name, ContentFile(encoded_text))
            job_obj.attachments.add(attachment_obj)


        error = None
        message = "Added to order ✔️"
        if len(attachment) > 0:
            #if user has uploded a file
            hasFile = True

            file_words = 0
            filename = str(attachment)
            if filename.lower().endswith(('.txt')):
                #if the uploaded file is .txt file
                for line in attachment:
                    #exclude the words between "[[[" and "]]]" from the word count.
                    try:
                        first, _, rest = line.decode('utf8').partition('[[[')
                        _, _, rest = rest.partition(']]]')
                        line = ' '.join([first.strip(), rest.strip()])     
                        file_words += len(line.split())
                    except UnicodeDecodeError:
                        #file file not utf8 encoded.
                        error= "File not supported!"
            if error == None:
                #add attachment to the Job
                attachment_obj = Attachment.objects.create(owner=request.user, word_count=file_words, orignal_filename=str(attachment), file = attachment)    
                job_obj.attachments.add(attachment_obj) 
                message = "Added to order ✔️" 
            else:
                message = error

        #get serialized data for attachment including the newly attached ones       
        serailzed_data = serializers.attachmentSerializer(job_obj.attachments.all(), many=True).data      
        if hasFile == True or hasText == True:
            #if user uploaded any one of text or file.
            return Response({"message": message, "data": serailzed_data}, status=status.HTTP_202_ACCEPTED)
        else:  
            #if user uploaded nothing           
            return Response({"message": "Add a .txt file or plain text", "data": serailzed_data}, status=status.HTTP_202_ACCEPTED)

    elif request.method == 'DELETE': #api/attchment/<str:attachment_id>
        '''
        remove(Delete) an attachment from a Job
        '''
        #get the Attachment object
        attachement_obj = Attachment.objects.get(attachment_id=attachment_id)  
        
        #Job of which this attachment was a part of
        related_job = attachement_obj.job_attachments.get()
   
        #delete the attachment
        attachement_obj.delete()

        #get the attachment left after deleting the one
        remaining_attachments = related_job.attachments.all()

        #get serialized data for attachments       
        serailzed_data = serializers.attachmentSerializer(remaining_attachments, many=True).data
        return Response(serailzed_data, status=status.HTTP_202_ACCEPTED)

 
from common.models import Language, Quality, Content
from payment_gateway.models import stripe_keys
from payment_gateway import verifiers
import stripe

#get stripe api key from database.

#from django.contrib.sites.models import Site
#current_site = Site.objects.get_current()
#YOUR_DOMAIN = "https://"+current_site.domain

@api_view(['PATCH', 'POST'])
@throttle_classes([AnonRateThrottle]) #Limiting number of API calls a user can make.
@authentication_classes([CsrfExemptSessionAuthentication, SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated]) #requires the request user to be authenticated
def job_api(request): 
    stripe.api_key = stripe_keys.objects.all().last().api_key
    ISO = request.LANGUAGE_CODE
    if request.method == 'PATCH': #api/job/language
        '''
        set source language of a job
        '''
        data = request.data
        job_id = data.get('job_id')
        source_language_id = data.get('source_language_id')

        job_obj = Job.objects.get(job_id=job_id)
        job_obj.source_language = Language.objects.get(pk=source_language_id)
        job_obj.save()
        return Response(status=status.HTTP_202_ACCEPTED)

    elif request.method == 'POST': #api/job/finalize
        '''
        set terget languages quality and content type of the Job, 
        calculate the total price and create the stripe checkout_session id
        '''
        data = request.data

        #get data from the request
        job_id = data.get('job_id')
        target_language_pks = request.POST.getlist('selectedLanguageIDs[]')
        selected_quality_pk = data.get('selectedQualityIDs')[0]
        selected_conten_type_pk = data.get('selectedContentTypeIDs')[0]
     
        #get Job object from databse for the job_id
        job_obj = Job.objects.get(job_id=job_id)

        #this API defaults to job_type="Translation" which needs to exists in database
        #for this API to work, it is auto created with the server is started, only way this
        #expetion can be triggested is if the job_type was manually deleted by admin.
        try:
            job_obj.job_type = JobType.objects.get(job_type="Translation")
        except:
            print('job_type="Translation" does not exist, everything will fail until this is fixed.')
            #TODO further handeling
            
        job_obj.quality = Quality.objects.get(pk = selected_quality_pk)
        job_obj.content = Content.objects.get(pk = selected_conten_type_pk)
        
        #clear previously assigned target language to assign new ones
        job_obj.target_language.clear()
        Contract.objects.all().filter(job=job_obj).delete()
        
        #assign target languages do the Job
        for target_language_pk in target_language_pks:
            job_obj.target_language.add(Language.objects.get(pk=int(target_language_pk)))
        
        #save all the changes to Job
        job_obj.save()
        #for target_language in job_obj.target_language.all():

        from common.models import Variables  
        from employee.models import Submissions  
        variable_obj = Variables.objects.last()
        company_share = variable_obj.company_share
        translator_share = variable_obj.translator_share
        proofreader_share = variable_obj.proofreader_share

        for target_language in job_obj.target_language.all():
            language_total = 0 #total price of attachment
            translation_submission_obj_list = []
            proofreading_submission_obj_list = []

            for attachment in job_obj.attachments.all():
                rate_obj = Rate.objects.get(source_language = job_obj.source_language, target_language = target_language, job_type= job_obj.job_type)
                attachment_price_for_perticular_language = rate_obj.base_rate * job_obj.quality.rate_multiplier * attachment.word_count
                language_total += attachment_price_for_perticular_language
                if job_obj.quality.proofreading == True:
                    translation_submission_obj = Submissions.objects.create(refrence_attachment=attachment, target_language=target_language, final = False)
                    translation_submission_obj_list.append(translation_submission_obj)
                    proofreading_submission_obj_list.append(Submissions.objects.create(refrence_attachment=attachment, target_language=target_language, final = True,  proofreading_contract=True, submission_dependency = translation_submission_obj))
                else:
                    translation_submission_obj_list.append(Submissions.objects.create(refrence_attachment=attachment, target_language=target_language, final = True))
            
            language_total = float(language_total)
            if job_obj.quality.proofreading == True:
                company_gets = (company_share/100)*language_total
                remaining = language_total - company_gets
                translator_gets = (translator_share/100)*remaining
                proofreader_gets = (proofreader_share/100)*remaining
                
                translation_contract_obj = Contract.objects.create(job=job_obj, target_language=target_language, status="TR", contract_price = translator_gets)
                proofreader_contract_obj = Contract.objects.create(final = True, job=job_obj,target_language=target_language, status="PF", dependency=translation_contract_obj, contract_price = proofreader_gets)

                for submission_obj in translation_submission_obj_list:
                    translation_contract_obj.submissions.add(submission_obj)
                
                print(proofreading_submission_obj_list)
                for submission_obj in proofreading_submission_obj_list:
                    print(submission_obj)

                    proofreader_contract_obj.submissions.add(submission_obj)

            else:
                company_gets = (company_share/100)*language_total
                remaining = language_total - company_gets
                translation_contract_obj = Contract.objects.create(final = True, job=job_obj, target_language=target_language, status="TR", contract_price = remaining)
                for submission_obj in translation_submission_obj_list:
                    translation_contract_obj.submissions.add(submission_obj)
        
        
        
        #add each attachment individually to the stripe order for 
        #better user understanding and transparency
        line_items = []
        for attachment in job_obj.attachments.all():
            attachment_total = 0 #total price of attachment
            for target_language in job_obj.target_language.all():
                rate_obj = Rate.objects.get(source_language = job_obj.source_language, target_language = target_language, job_type= job_obj.job_type)
                language_price = rate_obj.base_rate * job_obj.quality.rate_multiplier * attachment.word_count
                attachment_total += language_price
            
            attachment.price = attachment_total
            attachment.save()
            data = {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(round(attachment_total*100)), #attachment_total is in dollars, we convert it to cents
                        'product_data': {
                            'name': 'Translation of {} ({} words) from {} to {}'.format(attachment.orignal_filename, attachment.word_count, job_obj.source_language, job_obj.targetLanguageToString),
                            'images': [],
                        },
                    },
                    'quantity': 1,
                }
            line_items.append(data) #add attachment to order

        scheme = request.is_secure() and "https" or "http"
        from django.contrib.sites.models import Site
        current_site = Site.objects.get_current()
        YOUR_DOMAIN = scheme+"://"+current_site.domain
        

        try:
            #create checkout_session for stripe
            checkout_session = stripe.checkout.Session.create(
                customer_email= job_obj.employeer.email,
                client_reference_id=job_obj.job_id,
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                
                #redirect to create order step-2 screen if user cancel the payment
                cancel_url="{DOMAIN}/{ISO}/order/step-2/{JOB_ID}".format(DOMAIN=YOUR_DOMAIN, ISO=ISO, JOB_ID=job_id),
                #if the payment is successfully "processed" (might or might not be received , to verify 
                #if payment is received  is listen to stripe's webhook [in payment_gateway app] for confirmation) 
                #unique and temporary payment_token is passed in success_url to ensure security.  
                success_url="{DOMAIN}/{ISO}/order/success/{JOB_ID}/{TOKEN}".format(DOMAIN=YOUR_DOMAIN, ISO=ISO, JOB_ID=job_id, TOKEN=verifiers.create_payment_token(job_obj)),
            )
            return Response({'id': checkout_session.id}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_200_OK )


