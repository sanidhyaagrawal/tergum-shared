from django.urls import path

from . import views, apis

app_name = 'profiles'
#Contains views for screen which are customized to user's profile, such as dahsboard. 

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'), #get user's dashboard
    path('jobs/details/<str:job_id>', views.jobs_details, name='jobs_details'), #show user details for the job they created
    path('contract/feedback/<str:contract_id>', views.feedback, name='feedback'), #view for providing feedback for a contract
    
    #apis
    path('api/jobs/chat/send/', apis.post_message, name='post_message'), #POST | API to send a message to chat window
    path('api/jobs/chat/get/', apis.load_chat, name='load_chat'), #POST | API to load chat window
    path('api/contract/feedback/', apis.feedback, name='feedback'), #POST | API to send feedback for a contract

]


