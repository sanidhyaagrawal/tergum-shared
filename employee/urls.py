from django.urls import path

from . import views, apis

app_name = 'profiles'
#Contains views for screen which are customized to user's profile, such as dahsboard. 

urlpatterns = [
    #views
    path('contracts/accepted', views.accepted_contracts, name='accepted_contracts'), #view accpeted contracts
    path('contracts/completed', views.completed_contracts, name='accepted_contracts'), #view completed contracts
    path('contracts/feedback', views.feedback, name='feedback'), #view feedback for all the contracts
    path('translator/invitation/<str:email>/<str:token>', views.invite_link, name='invite_link'), #accept translator invitation 
    path('translator/invitation/expired', views.invite_link_expired, name='invite_link_expired'), #invalid invite link
    path('employee/contract/details/<str:contract_id>', views.contract_details, name='contract_details'), #view accepted contract details
    path('translator/settings', views.settings, name='settings'), #view profile -setting


    #apis
    path('api/translator/account/activate/', apis.accpet_invite, name='accpet_invite'), #POST | API to activate account from invite link
    path('api/translator/contract/sign/', apis.sign_contract, name='sign_contract'), #POST | API to accept a contract
    path('api/translator/contract/file/submit/', apis.create_submission, name='create_submission'), #POST | API to submit a file for a contract
    path('api/translator/contract/complete/', apis.mark_contract_completed, name='mark_contract_completed'), #POST | API to mark the contract as complete
    path('api/translator/edit', apis.edit_profile_details, name='edit_profile_details'), #PATCH | API to save changes to profile via settings


]



                            