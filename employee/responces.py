from rest_framework.response import Response
from rest_framework import status


#centralized responces for all the APIs for this app (users)
#is used for internationalization of responses
def getResponce(*args):
    responces = {
    "en" : {
        "invalid_contract_id" : Response({'error': "Invalid contract, try again"}, status=status.HTTP_200_OK),
        "alredy_signed" : Response({'error': "Contract is no longer avaiable, please refresh "}, status=status.HTTP_200_OK),
        "not_completed" : Response({'error': "Contract is not completed."}, status=status.HTTP_200_OK),
        "unauthorised" : Response({'error': "You don't have permisson to make changes to this contract."}, status=status.HTTP_200_OK),
        "signup_no_password" : Response({'error': "Input Password"}, status=status.HTTP_200_OK),
        "signup_short_password" : Response({'error': "Password must be atlest 5 characters"}, status=status.HTTP_200_OK),
        "signup_password_not_match" : Response({'error': "Password does not mach"}, status=status.HTTP_200_OK),
        "account_not_active" : Response({'error': "Your account is not activated, please contact admin."}, status=status.HTTP_200_OK),
      
        "email_not_sent" : Response({'error': "Couldn't send email, please try again."}, status=status.HTTP_200_OK),

      
        },
    }
    if responces.get(args[0]) != None: #ISO Code Exists
        return responces[args[0]][args[1]]
    else:    
        #ISO code not supported, end user will never face this error, just for exception handling in development.
        return Response({'error': "Invalid ISO code, supported codes are- 'en'"}, status=status.HTTP_400_BAD_REQUEST)