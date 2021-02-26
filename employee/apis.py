from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import auth
from django.http import JsonResponse

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework import status


#centralized responces for all the APIs for this app (users)
#is used for internationalization of responses
from users.responces import getResponce
from core.authenticators import CsrfExemptSessionAuthentication

from users.models import User

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login
from administrator.models import invite_links

@api_view(['POST'])
@authentication_classes([CsrfExemptSessionAuthentication, SessionAuthentication, BasicAuthentication])
def accpet_invite(request):
    from users.responces import getResponce
    ISO = request.LANGUAGE_CODE
    print(request.POST)
    email = request.POST['email'].strip()
    token = request.POST['token'].strip()
    if User.objects.all().filter(email=email.strip()).exists():
        user_obj = User.objects.get(email=email.strip())
    if invite_links.objects.all().filter(user=user_obj, token=token).exists():
        link_obj = invite_links.objects.get(user=user_obj, token=token)
        if user_obj.is_active == False:
            password = request.POST['password'].strip()
            repassword = request.POST['repassword'].strip()
            if len(password)==0:
                return getResponce(ISO, 'signup_no_password')


            elif len(password)<5:
                return getResponce(ISO, 'signup_short_password')

            
            elif password != repassword:
                return getResponce(ISO, 'signup_password_not_match')

            user_obj.is_active = True
            user_obj.set_password(password)
            user_obj.save()
            login(request, user_obj, backend='django.contrib.auth.backends.ModelBackend')

            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_205_RESET_CONTENT) #link expired
    else:
        return Response(status=status.HTTP_205_RESET_CONTENT) #link expired

from services.verifiers import contract_id_is_valid
from django.utils import timezone
@api_view(['POST'])
@authentication_classes([CsrfExemptSessionAuthentication, SessionAuthentication, BasicAuthentication])
def sign_contract(request):
    from employee.responces import getResponce
    ISO = request.LANGUAGE_CODE
    contract_id = request.POST['contract_id'].strip()
    print(contract_id)
    is_vaild, contract_obj = contract_id_is_valid(contract_id)
    if is_vaild:
        if contract_obj.is_signed == False:
            contract_obj.profile = request.user
            contract_obj.is_signed = True
            contract_obj.signing_date =  timezone.now()
            contract_obj.save()
            return Response({"contract_id": contract_id}, status=status.HTTP_202_ACCEPTED)
        else:
         return getResponce(ISO, 'alredy_signed')
    else:
        return getResponce(ISO, 'invalid_contract_id')



from services.verifiers import contract_id_is_valid
from django.utils import timezone
from profiles.models import Profile
from users.username_validator import check_or_get_username

@api_view(['POST'])
@authentication_classes([CsrfExemptSessionAuthentication, SessionAuthentication, BasicAuthentication])
def edit_profile_details(request):
    from users.responces import getResponce

    ISO = request.LANGUAGE_CODE
    data = request.data
    first_name = data['first_name'].strip()
    last_name = data['last_name'].strip()
    bio = data['bio'].strip()
    username = data['username'].strip()
    country = data['country'].strip()
    city = data['city'].strip()
    
    if len(first_name)==0 and len(last_name)==0:
        return user.responces.getResponce(ISO, 'signup_name_required')

    elif len(first_name)==0:
        return getResponce(ISO, 'signup_no_firstname')
    
    elif len(last_name)==0:
        return getResponce(ISO, 'signup_no_lastname')

    profile_obj = Profile.objects.get(user = request.user)
    if len(data.get('first_name')) == 0:
            return getResponce(ISO, 'username_unavaiable')

    request.user.first_name = first_name
    request.user.last_name = last_name
    if request.user.username != username:
        is_available, suggestions= check_or_get_username(username)
        if is_available:
            request.user.username = data.get('username')
        else:
            return getResponce(ISO, 'username_unavaiable')

    profile_obj.bio = bio
    profile_obj.country = country
    profile_obj.city = city
    if bool(data.get('profile')):
        profile_obj.image = data.get('profile')
    request.user.save()
    profile_obj.save()
    return Response(status=status.HTTP_202_ACCEPTED)








from common.models import Attachment
@api_view(['POST'])
@authentication_classes([CsrfExemptSessionAuthentication, SessionAuthentication, BasicAuthentication])
def create_submission(request):
    from employee.responces import getResponce
    ISO = request.LANGUAGE_CODE
    data = request.data
    attachment_id = data.get('attachment_id')
    contract_id = data.get('contract_id')
    submission = data.get('submission')
    print(data)
    is_vaild, contract_obj = contract_id_is_valid(contract_id)
    if is_vaild:
        if contract_obj.is_signed == True:
            if contract_obj.profile == request.user:
                attachment_obj = Attachment.objects.get(attachment_id = attachment_id)
                submission_obj = contract_obj.submissions.all().filter(refrence_attachment = attachment_obj)[0]

                error = None
                message = "Added to order ✔️"
                if len(submission) > 0:
                    #if user has uploded a file
                    hasFile = True

                    file_words = 0
                    filename = str(submission)
                    print(filename)
                    if filename.lower().endswith(('.txt')):
                        #if the uploaded file is .txt file
                        for line in submission:
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
                            #add submission to the Job
                            #submission_obj = Attachment.objects.create(owner=request.user, word_count=file_words, orignal_filename=str(submission), file = submission)    
                            #job_obj.submissions.add(submission_obj) 
                            #print(submission_obj)
                            submission_obj.submission_filename = str(submission)
                            submission_obj.submission_file = submission
                            submission_obj.submited_by = request.user
                            submission_obj.submit_date = timezone.now()
                            submission_obj.save()
                            message = "Added to order ✔️" 
                        else:
                            message = error
                        #get serialized data for submission including the newly attached ones       
                        #serailzed_data = serializers.submissionSerializer(job_obj.submissions.all(), many=True).data      
                        if hasFile == True:
                            #if user uploaded any one of text or file.
                            return Response({"message": message}, status=status.HTTP_202_ACCEPTED)
                    else:  
                        #if user uploaded nothing           
                        return Response({"message": "Add a .txt file"}, status=status.HTTP_200_OK)
                else:  
                    #if user uploaded nothing           
                    return Response({"message": "Add a .txt file"}, status=status.HTTP_200_OK)

                                
            else:
                return getResponce(ISO, 'invalid_contract_id')
        else:
            return getResponce(ISO, 'invalid_contract_id')
    else:
        return getResponce(ISO, 'invalid_contract_id')
 
    

from common.models import Attachment
@api_view(['POST'])
@authentication_classes([CsrfExemptSessionAuthentication, SessionAuthentication, BasicAuthentication])
def mark_contract_completed(request):
    from employee.responces import getResponce
    ISO = request.LANGUAGE_CODE
    data = request.data
    contract_id = data.get('contract_id')
    is_vaild, contract_obj = contract_id_is_valid(contract_id)
    if is_vaild:
        if contract_obj.is_signed == True:
            if contract_obj.profile == request.user:
                if contract_obj.all_submitted:
                    contract_obj.completed = True
                    contract_obj.completion_date = timezone.now()
                    contract_obj.save()
                    return Response(status=status.HTTP_202_ACCEPTED)

                else:
                    return getResponce(ISO, 'not_completed')                
            else:
                return getResponce(ISO, 'unauthorised')
        else:
            return getResponce(ISO, 'unauthorised')
    else:
        return getResponce(ISO, 'invalid_contract_id')
 
    

  
      