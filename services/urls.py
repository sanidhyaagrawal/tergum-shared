from django.urls import path

from . import views
from . import apis

app_name = 'application'
#Containes service specific views such as create order. 

urlpatterns = [
    path('order/create', views.create_order, name='create_order'), #Initiate (start) a new order
    path('order/step-1/<str:job_id>', views.order_step1, name='order_step1'), #Step-1 of creating an order
    path('order/step-2/<str:job_id>', views.order_step2, name='order_step2'), #Step-2 of creating an order
    path('order/delete/<str:job_id>', views.order_delete, name='order_delete'), #delete DRAFT order
    path('order/success/<str:job_id>/<str:token>', views.order_success, name='order_success'), #Stripe's redirect URL if the payment was "processed" successfully 

    #apis
    path('api/attchment_api', apis.attchment_api, name='attchment_api'), #POST | add attachement to DRAFT Job
    path('api/attchment/<str:attachment_id>', apis.attchment_api), #DELETE | delete attachement from the DRAFT Job
    path('api/job/language', apis.job_api), #PATCH | set source language of a job
    path('api/job/finalize', apis.job_api), #POST | finalize a job and proceed to pay

]






    
