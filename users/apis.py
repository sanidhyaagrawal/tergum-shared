from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import auth
from django.http import JsonResponse
from .models import User
from .validators import validateEmail

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework import status


#centralized responces for all the APIs for this app (users)
#is used for internationalization of responses
from users.responces import getResponce
from users.username_validator import check_or_get_username


@api_view(['POST'])
@throttle_classes([AnonRateThrottle]) #Limiting number of API calls a user can make.
def login_api(request): 
    '''
    Validates email and passowrd and login the user using session authentication. 
    '''
    ISO = request.LANGUAGE_CODE
    if request.method == 'POST':
        email = request.POST['email'].strip()
        password = request.POST['password'].strip()
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return Response(status=status.HTTP_202_ACCEPTED)
            else:
                return getResponce(ISO, 'account_not_active')
        else:
            return getResponce(ISO, 'login_invalid_credentials')
    else:
        return redirect('/verification')

@api_view(['POST'])
@throttle_classes([AnonRateThrottle]) #Limiting number of API calls a user can make.
def signup_api(request):
    '''
    gets user details and validates it, creates an account and login the user if eveything is valid.
    '''
    ISO = request.LANGUAGE_CODE
    if request.method == 'POST':
        firstname = request.POST['firstname'].strip()
        lastname = request.POST['lastname'].strip()
        email = request.POST['email'].strip()
        password = request.POST['password'].strip()
        repassword = request.POST['repassword'].strip()
        accepted, reason = validateEmail(email)
        
        if len(firstname)==0 and len(lastname)==0:
            return getResponce(ISO, 'signup_name_required')

        elif len(firstname)==0:
            return getResponce(ISO, 'signup_no_firstname')

        
        elif len(lastname)==0:
            return getResponce(ISO, 'signup_no_lastname')

        elif not accepted: #from validateEmail function
            return Response({'error': reason}, status=status.HTTP_200_OK)

        elif len(password)==0:
            return getResponce(ISO, 'signup_no_password')


        elif len(password)<5:
            return getResponce(ISO, 'signup_short_password')

        
        elif password != repassword:
            return getResponce(ISO, 'signup_password_not_match')

        else:
            #eveything is valid
            username = email.split("@")[0]
            is_available, suggestions= check_or_get_username(username)
            if is_available:
                username = username
            else:
                username = suggestions[0]
            user = User.objects.create_user(first_name = firstname, last_name=firstname, username=username, email = email, password =password)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return Response(status=status.HTTP_202_ACCEPTED)



from users.models import forget_password_links
# Create your models here.
from django.utils import timezone
from os import urandom 

#Custom validators for feilds like email.

def validatePassToken(token) :
    if forget_password_links.objects.all().filter(token = token).exists(): 
        forget_obj = forget_password_links.objects.get(token = token)
        import datetime
        if (forget_obj.time_created + datetime.timedelta(minutes=60)) >  timezone.now():
            return (True, 'Valid and Available', forget_obj)
        else:
            return (False,"Link has been expired.", None)
    else:
        return (False,"Invalid Link.", None)




def create_forgot_pass_token():
    token = urandom(32).hex()
    is_taken, reason, obj = validatePassToken(token)
    while is_taken:
        token = urandom(32).hex()
        is_taken, reason, obj = validatePassToken(token)
    return token

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

@api_view(['POST'])
@throttle_classes([AnonRateThrottle]) #Limiting number of API calls a user can make.
def forget_password(request): 
    ISO = request.LANGUAGE_CODE
    from users.responces import getResponce

    if request.method == 'POST':
        email = request.POST['email'].strip()
        try: 
            user_obj = User.objects.get(email = email)
        except:
            return getResponce(ISO, 'invalid_email')

        pass_obj = forget_password_links.objects.create(user=user_obj, time_created=timezone.now(), token=create_forgot_pass_token())
        scheme = request.is_secure() and "https" or "http"
        YOUR_DOMAIN = scheme+"://"+request.META['HTTP_HOST']
        
        try:
            subject = 'Password Recovery | Tergum'
            html_message = render_to_string('users/forget_password.html', {'user': user_obj, "link_obj":pass_obj, "domain":YOUR_DOMAIN})
            message = "We heard that you lost your Tergum password. Sorry about that!"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [ email,]
            send_mail( subject, message, email_from, recipient_list, html_message=html_message, fail_silently=False )
        except Exception as e:
            print(e)
            pass_obj.delete()
            return getResponce(ISO, 'email_not_sent')


        return Response(status=status.HTTP_202_ACCEPTED)
          
    else:
        return redirect('/verification')

from core.authenticators import CsrfExemptSessionAuthentication
from users.models import forget_password_links


@api_view(['POST'])
@authentication_classes([CsrfExemptSessionAuthentication, SessionAuthentication, BasicAuthentication])
def recover_password(request):
    from users.responces import getResponce
    ISO = request.LANGUAGE_CODE
    print(request.POST)
    token = request.POST['token'].strip()
    is_exist, reason, token_obj = validatePassToken(token)
    
    if  is_exist:
            user_obj = token_obj.user
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
