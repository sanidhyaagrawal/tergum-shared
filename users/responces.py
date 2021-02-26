from rest_framework.response import Response
from rest_framework import status


#centralized responces for all the APIs for this app (users)
#is used for internationalization of responses
def getResponce(*args):
    responces = {
    "en" : {
        "login_invalid_credentials" : Response({'error': "Invalid credentials, try again"}, status=status.HTTP_200_OK),
        "signup_name_required" : Response({'error': "First & last name are reqired"}, status=status.HTTP_200_OK),
        "signup_no_firstname" : Response({'error': "First name is reqired"}, status=status.HTTP_200_OK),
        "signup_no_lastname" : Response({'error': "Last name is reqired"}, status=status.HTTP_200_OK),
        "signup_no_password" : Response({'error': "Input Password"}, status=status.HTTP_200_OK),
        "signup_short_password" : Response({'error': "Password must be atlest 5 characters"}, status=status.HTTP_200_OK),
        "signup_password_not_match" : Response({'error': "Password does not mach"}, status=status.HTTP_200_OK),
        "account_not_active" : Response({'error': "Your account is not activated, please contact admin."}, status=status.HTTP_200_OK),
        "username_unavaiable" : Response({'error': "This username is not available"}, status=status.HTTP_200_OK),

        "email_not_sent" : Response({'error': "Couldn't send email, please try again."}, status=status.HTTP_200_OK),

      
        },
    }
    if responces.get(args[0]) != None: #ISO Code Exists
        return responces[args[0]][args[1]]
    else:    
        #ISO code not supported, end user will never face this error, just for exception handling in development.
        return Response({'error': "Invalid ISO code, supported codes are- 'en'"}, status=status.HTTP_400_BAD_REQUEST)