from django.urls import path

from . import views, apis

app_name = 'profiles'
#Contains views for screen which are customized to user's profile, such as dahsboard. 

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'), #get user's dashboard
    path('jobs/details/<str:job_id>', views.jobs_details, name='jobs_details'), #get user's dashboard
    path('contract/feedback/<str:contract_id>', views.feedback, name='feedback'), #get user's dashboard
    
    #apis
    path('api/jobs/chat/send/', apis.post_message, name='post_message'), #get user's dashboard
    path('api/jobs/chat/get/', apis.load_chat, name='load_chat'), #get user's dashboard
    path('api/contract/feedback/', apis.feedback, name='feedback'), #get user's dashboard

]


