from django.urls import path

from . import views, apis

app_name = 'profiles'
#Contains views for screen which are customized to user's profile, such as dahsboard. 

urlpatterns = [
    path('contracts/accepted', views.accepted_contracts, name='accepted_contracts'), #get user's dashboard
    path('contracts/completed', views.completed_contracts, name='accepted_contracts'), #get user's dashboard
    #path('contracts/accepted/details/<str:job_id>', views.accepted_contracts_details, name='accepted_contracts_details'), #get user's dashboard
    #path('contracts/completed/details/<str:job_id>', views.completed_contracts_details, name='accepted_contracts_details'), #get user's dashboard
    path('translator/invitation/<str:email>/<str:token>', views.invite_link, name='invite_link'), #get user's dashboard
    path('translator/invitation/expired', views.invite_link_expired, name='invite_link_expired'), #get user's dashboard
    path('employee/contract/details/<str:contract_id>', views.contract_details, name='contract_details'), #get user's dashboard
    path('translator/settings', views.settings, name='settings'), #get user's dashboard


    #apis
    path('api/translator/account/activate/', apis.accpet_invite, name='accpet_invite'), #get user's dashboard
    path('api/translator/contract/sign/', apis.sign_contract, name='sign_contract'), #get user's dashboard
    path('api/translator/contract/file/submit/', apis.create_submission, name='create_submission'), #get user's dashboard
    path('api/translator/contract/complete/', apis.mark_contract_completed, name='mark_contract_completed'), #get user's dashboard
    path('api/translator/edit', apis.edit_profile_details, name='edit_profile_details'), #get user's dashboard


]



                            