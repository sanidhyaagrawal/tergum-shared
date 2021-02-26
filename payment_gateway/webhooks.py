#stripe_websocket
import stripe
from payment_gateway.models import stripe_keys
from django.views.decorators.csrf import csrf_exempt

# Using Django
from django.http import HttpResponse

# Interal Apps
from services.models import Job, JobType
from common.models import Status

def order_mark_paid(session):
    print("order_mark_paid")
    job_id = session["client_reference_id"]
    job_obj = Job.objects.get(job_id=job_id)
    job_obj.paid = True
    job_obj.status = Status.objects.create(status_name="OP", comment="Payment succesfull! Waitng for translators to pick up the job.")
    job_obj.save()

def order_mark_accepted(session):
    print("order_mark_accepted")
    job_id = session["client_reference_id"]
    job_obj = Job.objects.get(job_id=job_id)
    job_obj.status = Status.objects.create(status_name="PN", comment="Awaiting payment confirmation from Stripe, this might take a few minutes.")
    job_obj.accepted = True
    job_obj.save()

def email_customer_about_failed_payment(session):
  # TODO: send email to user about payment failed
  print("Emailing customer")

@csrf_exempt
def stripe_webhook(request):

  #get stripe api key from database
  stripe.api_key = stripe_keys.objects.all().last().api_key

  # You can find your endpoint's secret in your webhook settings
  endpoint_secret = stripe_keys.objects.all().last().endpoint_secret
  payload = request.body
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None
  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, endpoint_secret
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return HttpResponse(status=400)
 

  # Handle the checkout.session.completed event
  if event['type'] == 'checkout.session.completed':
    session = event['data']['object']

    # Mark the order in your database as accepted, we are still awaiting payment 
    # (still waiting for funds to be transferred from the customer's account.)
    order_mark_accepted(session)

    # Check if the order is already paid (e.g., from a card payment)
    # A delayed notification payment will have an `unpaid` status
    if session.payment_status == "paid":
      # Mark order as paid
      order_mark_paid(session)

  #delayed payment recived
  elif event['type'] == 'checkout.session.async_payment_succeeded':
    session = event['data']['object']
    # Mark order as paid
    order_mark_accepted(session)

  #delayed payment failed
  elif event['type'] == 'checkout.session.async_payment_failed':
    session = event['data']['object']

    #Send an email to the customer asking them to retry their order
    email_customer_about_failed_payment(session)

  #Passed signature verification (Inform stripe that we have successfully received the message)
  return HttpResponse(status=200)


