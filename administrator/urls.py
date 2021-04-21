from django.urls import path

from . import views, apis

app_name = 'profiles'
#Contains views for screen which are customized to user's profile, such as dahsboard. 

urlpatterns = [
    path('admin/translator/create', views.create_translator, name='create_translator'), #create user page
    path('admin/translator/view', views.view_employee, name='view_employee'), #view all active translators
    path('admin/jobs/available', views.available_jobs, name='available_jobs'), #view list of all unassigned jobs
    path('admin/jobs/details/<str:job_id>', views.available_jobs_details, name='available_jobs_details'), #view job details for a perticular job
    path('admin/contracts/completed', views.completed_contracts, name='completed_contracts'), #view list of all complete jobs
    path('admin/contracts/accepted', views.accepted_contracts, name='accepted_contracts'), #view list of all assigned but not completed jobs
    path('admin/translator/<str:username>/contracts/completed/due', views.translator_completed_contracts_due, name='completed_contracts_due'), #view due payments for a translatpr
    path('admin/translator/<str:username>/contracts/completed/paid', views.translator_completed_contracts_paid, name='completed_contracts_paid'), #view payment history for a translatpr
    path('admin/translator/<str:username>/details', views.view_employee_details, name='view_employee_details'), #view profile of a translator
    path('admin/translator/<str:username>/contracts/accepted', views.translator_accepted_contracts, name='translator_accepted_contracts'), #view accepted contracts by a translator
    path('admin/translator/<str:username>/contracts/completed/all', views.translator_completed_contracts_all, name='translator_completed_contracts_all'), #view completed contracts by a translator
    path('admin/translator/edit', views.edit_employee, name='edit_employee'), #edit translator details
    
    
    #apis
    path('api/translator/create/', apis.create_translator, name='create_translator'), #POST | API to create translators
    path('api/contract/assign/', apis.contract_assign, name='contract_assign'), #POST | API to assign a contract to a translator
    path('api/contract/paid/', apis.contract_paid, name='contract_paid'), #POST | API to mark a contract as paid



]