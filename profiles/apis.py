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
from common.models import Notifications
from django.utils import timezone

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

    job_obj = Job.objects.get(job_id=job_id)
    message_obj = Message.objects.create(text=text, user=request.user, employee= request.user.is_staff)
    job_obj.chat.add(message_obj)
    data = messageSerializer(job_obj.chat.all(), many=True).data
    contracts = Contract.objects.all().filter(job=job_obj)
    if request.user.is_staff:
        Notifications.objects.create(target=job_obj.employeer, creation_date=timezone.now(), text="You have a new message.", icon="fas fa-envelope", colour="primary", link="/jobs/details/{}".format(job_obj.job_id))
    else:
        for contract in contracts:
            if contract.is_signed:
                Notifications.objects.create(target=contract.profile, creation_date=timezone.now(), text="You have a new message.", icon="fas fa-envelope", colour="primary", link="/employee/contract/details/{}".format(contract.contract_id))

    return Response(data, status=status.HTTP_202_ACCEPTED)

    
@api_view(['POST'])
@authentication_classes([CsrfExemptSessionAuthentication, SessionAuthentication, BasicAuthentication])
def load_chat(request):
    from users.responces import getResponce
    ISO = request.LANGUAGE_CODE
    job_id = request.POST['job_id']
    job_obj = Job.objects.get(job_id=job_id)
    data = messageSerializer(job_obj.chat.all(), many=True).data
    return Response(data, status=status.HTTP_202_ACCEPTED)


    
@api_view(['POST'])
@authentication_classes([CsrfExemptSessionAuthentication, SessionAuthentication, BasicAuthentication])
def feedback(request):
    from users.responces import getResponce
    ISO = request.LANGUAGE_CODE
    contract_id = request.POST['contract_id']
    feedback = request.POST['message']
    rating = request.POST['rating']

    if float(rating) > 0 and float(rating) <= 5:
        contract_obj = Contract.objects.get(contract_id=contract_id)
        contract_obj.rating = rating
        contract_obj.feedback = feedback
        contract_obj.save()
        Notifications.objects.create(target=contract_obj.profile, creation_date=timezone.now(), text="Client provided you feedback and rating", icon="fas fa-star",  colour="success", link="/contracts/feedback")
        return Response(status=status.HTTP_202_ACCEPTED)

    else:
        return Response({"error": "Please provide star rating"}, status=status.HTTP_200_OK)
    return Response( status=status.HTTP_202_ACCEPTED)


    
  
      