
from django.shortcuts import render, redirect
from services.models import Job
from django.utils import timezone
import pytz
import datetime
from services.models import Contract
from profiles.models import Profile
from django.contrib import messages

def dashboard(request):
    '''
    Render customized dashboard based on type of the 
    request user like admin, employee or customer
    '''
    
    #Temporoy comments for devleopment purpose
    '''
    if request.user.is_superuser and request.user.is_active:
        return render(request, 'admin/dashboard.html')
    elif request.user.is_staff and request.user.is_active:
        return render(request, 'employees/dashboard.html')
    ''' 
    print(request.user.is_superuser)
    if request.user.is_superuser and request.user.is_active:
        return render(request, 'administrator/admin_dashboard.html')
    elif request.user.is_staff and request.user.is_active:
        translation_contracts = []
        proofreading_contracts = []
        profile_obj = Profile.objects.get(user=request.user)
        completed_contracts = Contract.objects.all().filter(profile=request.user, completed=True)
        total_earning = 0
        for contract in completed_contracts:
            total_earning += contract.contract_price
        ongoing_projects = Contract.objects.all().filter(profile=request.user, completed=False).count()
        for from_language in profile_obj.from_languages.all():
            for to_language in profile_obj.to_languages.all():
                translation_contracts.extend(Contract.objects.all().filter(dependency = None, is_signed=False, target_language=to_language, job__source_language = from_language, job__paid = True))
                proofreading_contracts.extend(Contract.objects.all().filter(dependency__completed = True, is_signed=False, target_language=to_language, job__source_language = from_language, job__paid = True))
        return render(request, 'employee/translator_dashboard.html', {"translation_contracts":translation_contracts, "proofreading_contracts":proofreading_contracts, "total_earning":total_earning, "ongoing_projects":ongoing_projects})
    
    elif request.user.is_active:
        #customer's dashboard
        active_jobs = Job.objects.all().filter(employeer=request.user, accepted=True).exclude(status__status_name="DN")
        draft_jobs = Job.objects.all().filter(employeer=request.user, accepted=False)
        completed_jobs = Job.objects.all().filter(employeer=request.user, status__status_name="DN")
        active_drafts = []

        for draft in draft_jobs:
            if len(draft.attachments.all()) > 0:
                #if the Draft has attachments, we add it to once that'll 
                #be shown on the dashbaord
                active_drafts.append(draft)
            else:
                # if the draft has no attachments, we check if it's been more than 24
                # hours since the job was created, if yes we delete the draft.
                # We do this as a person while creating an order on one tab 
                # might open the dashboard on other, if we do impose 
                # this check, it will delete the order the user was just about to add
                # an attachment to. 
                if draft.posted_date + datetime.timedelta(hours=24) >  timezone.now():
                    draft.delete()   
        #messages.add_message(request, messages.INFO, 'Something went wrong, try again later.') 

        #render customer's dashboard with requied data
        return render(request, 'customer/dashboard.html', {"active_jobs":active_jobs, "draft_jobs":active_drafts, "completed_jobs":completed_jobs})
    else:
        return redirect("/login") #TODO replace with view url lookups.      
            
            
            
def feedback(request, contract_id):
    if request.user.is_active:
        contract_obj = Contract.objects.get(contract_id=contract_id)
        return render(request, 'base/404.html', {"contract_obj":contract_obj})
    else:
        return redirect("/login") #TODO replace with view url lookups. 

def jobs_details(request, job_id):
    if request.user.is_active:
        job_obj = Job.objects.get(job_id=job_id)
        contracts = Contract.objects.all().filter(job=job_obj)
        #all_employees = Profile.objects.all().filter(title="TR")

        return render(request, 'base/404.html',{"job_obj":job_obj, "contracts":contracts})
    else:
        return redirect("/login") #TODO replace with view url lookups. 