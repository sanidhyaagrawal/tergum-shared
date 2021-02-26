from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework import status


from core.authenticators import CsrfExemptSessionAuthentication

from django.contrib.auth.models import auth
from services.models import Message, Job, Contract
from .serializers import messageSerializer

@api_view(['POST'])
@authentication_classes([CsrfExemptSessionAuthentication, SessionAuthentication, BasicAuthentication])
def post_message(request):
    from users.responces import getResponce
    ISO = request.LANGUAGE_CODE
    print(request.POST)
    text = request.POST['message'].strip()
    job_id = request.POST['job_id']
    if len(text) == 0:
        return Response({"error": "Please type something"},status=status.HTTP_200_OK)

    print(job_id)
    job_obj = Job.objects.get(job_id=job_id)
    message_obj = Message.objects.create(text=text, user=request.user, employee= request.user.is_staff)
    job_obj.chat.add(message_obj)
    data = messageSerializer(job_obj.chat.all(), many=True).data
    print(data)
    '''   
    from common.models import Notifications
    from django.utils import timezone
    Notifications.objects.create(user=request.user, creation_date= timezone.now(), link= "", text="New message in accepted contract.")
    '''
    return Response(data, status=status.HTTP_202_ACCEPTED)

    
@api_view(['POST'])
@authentication_classes([CsrfExemptSessionAuthentication, SessionAuthentication, BasicAuthentication])
def load_chat(request):
   
    from users.responces import getResponce
    ISO = request.LANGUAGE_CODE
    print(request.POST)
    job_id = request.POST['job_id']
    job_obj = Job.objects.get(job_id=job_id)
    data = messageSerializer(job_obj.chat.all(), many=True).data
    return Response(data, status=status.HTTP_202_ACCEPTED)


    
@api_view(['POST'])
@authentication_classes([CsrfExemptSessionAuthentication, SessionAuthentication, BasicAuthentication])
def feedback(request):
 
    from users.responces import getResponce
    ISO = request.LANGUAGE_CODE
    print(request.POST)
    contract_id = request.POST['contract_id']
    feedback = request.POST['message']
    rating = request.POST['rating']

    if int(rating) > 0 and int(rating) <= 5:
        contract_obj = Contract.objects.get(contract_id=contract_id)
        contract_obj.rating = rating
        contract_obj.feedback = feedback
        contract_obj.save()

    else:
        return Response({"error": "Please provide star rating"}, status=status.HTTP_200_OK)
    return Response( status=status.HTTP_202_ACCEPTED)


    
  
      