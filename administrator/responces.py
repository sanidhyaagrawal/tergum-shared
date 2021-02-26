from rest_framework.response import Response
from rest_framework import status


#centralized responces for all the APIs for this app (users)
#is used for internationalization of responses
def getResponce(*args):
    responces = {
    "en" : {
        "contract_alredy_signed" : Response({'error': "This contract is alredy signed, please refresh."}, status=status.HTTP_200_OK),
        "contract_not_complete" : Response({'error': "This contract is not yet completed, please look into logs."}, status=status.HTTP_200_OK),
       
        },
    }
    if responces.get(args[0]) != None: #ISO Code Exists
        return responces[args[0]][args[1]]
    else:    
        #ISO code not supported, end user will never face this error, just for exception handling in development.
        return Response({'error': "Invalid ISO code, supported codes are- 'en'"}, status=status.HTTP_400_BAD_REQUEST)