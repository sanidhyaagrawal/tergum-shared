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
from users.responces import getResponce

#import secrets
from os import urandom 

#centralized responces for all the APIs for this app (users)
#is used for internationalization of responses
from users.responces import getResponce
from users.validators import validateEmail
from users.username_validator import check_or_get_username
from users.models import User
from common.models import Language, Content
from profiles.models import Profile
from core.authenticators import CsrfExemptSessionAuthentication
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import invite_links
@api_view(['POST'])
@throttle_classes([AnonRateThrottle]) #Limiting number of API calls a user can make.
@authentication_classes([CsrfExemptSessionAuthentication, SessionAuthentication, BasicAuthentication])



#TODO Admin Only Authentication
#TODO Admin Only Authentication
#TODO Admin Only Authentication
#TODO Admin Only Authentication
#TODO Admin Only Authentication

def create_translator(request): 
    '''
    Validates email and passowrd and login the user using session authentication. 
    '''
    ISO = request.LANGUAGE_CODE
    if request.method == 'POST':
        data = request.data
        
        firstname = data.get('first_name')
        lastname = data.get('last_name')
        #username = data.get('username')
        email = data.get('email')
        #password = data.get('password')
        content_type_pks = request.POST.getlist('skills[]')
        source_language_pks = request.POST.getlist('source_languages[]')
        target_language_pks = request.POST.getlist('target_languages[]')
        accepted, reason = validateEmail(email)
        print(source_language_pks,target_language_pks,content_type_pks )
        password = urandom(32).hex() #temporary random password, user can not log-in using this

        if len(firstname)==0 and len(lastname)==0:
            return getResponce(ISO, 'signup_name_required')

        elif len(firstname)==0:
            return getResponce(ISO, 'signup_no_firstname')
        
        elif len(lastname)==0:
            return getResponce(ISO, 'signup_no_lastname')

        elif not accepted: #from validateEmail function
            return Response({'error': reason}, status=status.HTTP_200_OK)
        
        else:
            #eveything is valid
            #username = email.split("@")[0] #temporary username
            is_available, suggestions= check_or_get_username(firstname)
            if is_available:
               username = firstname
            else:
                username= suggestions[0]
            
            
            user = User.objects.create_user(is_staff=True, is_active= False, first_name = firstname, last_name=lastname, username=username, email = email, password =password)
            profile = Profile.objects.get(user=user)
            #assign target languages do the Job
            for language_pk in source_language_pks:
                #print(language_pk)
                profile.from_languages.add(Language.objects.get(pk=int(language_pk)))
            
            for language_pk in target_language_pks:
                #print(language_pk)

                profile.to_languages.add(Language.objects.get(pk=int(language_pk)))
            
            for content_pk in content_type_pks:
                #print(content_pk)
                profile.content_types.add(Content.objects.get(pk=int(content_pk)))
            
            link_obj = invite_links.objects.create(user=user, token=urandom(10).hex())
            try:
                subject = 'Welcome to Tergum | Employee Registration'
                html_message = render_to_string('administrator/email_employee_registration.html', {'user': user, "link_obj":link_obj})
                message = strip_tags(html_message)
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [ email,]
                send_mail( subject, message, email_from, recipient_list, html_message=html_message, fail_silently=False )
            except Exception as e:
                print(e)
                profile.delete()
                user.delete()
                return getResponce(ISO, 'email_not_sent')
            return Response(status=status.HTTP_202_ACCEPTED)
    else:
        return redirect('/verification')



from services.models import Contract, Job

@api_view(['POST'])
@throttle_classes([AnonRateThrottle]) #Limiting number of API calls a user can make.
@authentication_classes([CsrfExemptSessionAuthentication, SessionAuthentication, BasicAuthentication])
def contract_assign(request): 
    '''
    Assign a contract to a employee
    '''
    from administrator.responces import getResponce
    from django.utils import timezone

    ISO = request.LANGUAGE_CODE
    if request.method == 'POST':
        data = request.data
        empID = data.get('empID')
        cID = data.get('cID')
        print(cID, empID)
        user_obj = User.objects.get(username=empID)
        contract_obj = Contract.objects.get(contract_id=cID)
        if contract_obj.is_signed == False:
            contract_obj.profile = user_obj
            contract_obj.is_signed = True
            contract_obj.signing_date =  timezone.now()
            contract_obj.save()
            return Response(status=status.HTTP_202_ACCEPTED)

        else:
            return getResponce(ISO, 'contract_alredy_signed')
            
    else:
        return redirect('/verification')



from services.models import Contract, Job

@api_view(['POST'])
@throttle_classes([AnonRateThrottle]) #Limiting number of API calls a user can make.
@authentication_classes([CsrfExemptSessionAuthentication, SessionAuthentication, BasicAuthentication])
def contract_paid(request): 
    '''
    Assign a contract to a employee
    '''
    from administrator.responces import getResponce
    from django.utils import timezone

    ISO = request.LANGUAGE_CODE
    if request.method == 'POST':
        data = request.data
        cID = data.get('contract_id')
        print(cID)
        contract_obj = Contract.objects.get(contract_id=cID)
        if contract_obj.completed == True:
            contract_obj.paid = True
            contract_obj.save()
            return Response(status=status.HTTP_202_ACCEPTED)

        else:
            return getResponce(ISO, 'contract_not_complete')
            
    else:
        return redirect('/verification')





