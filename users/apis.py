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


