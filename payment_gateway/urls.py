from django.urls import path

from . import webhooks

app_name = 'payment_gateway'
#Containes service specific views such as create order. 

'''
Stripe uses webhooks to notify your application when an event happens 
in your account. Webhooks are particularly useful for asynchronous 
events like when a customer’s bank confirms a payment, a customer 
disputes a charge, or a recurring payment succeeds
'''

urlpatterns = [
    path('ws/stripe/webhooks', webhooks.stripe_webhook), #Endpoint for listening to Stripe webhook
]






    
