
from django.shortcuts import render, redirect
from services.models import Job
from django.utils import timezone
import pytz
import datetime
from services.models import Contract
from profiles.models import Profile
from django.contrib import messages
from common.models import Notifications
from users.models import User

def dashboard(request):
    '''
    Render customized dashboard based on type of the 
    request user like admin, employee or customer
    '''
     
    print(request.user.is_superuser)
    if request.user.is_superuser and request.user.is_active: #Admin
        
        notifications = Notifications.objects.all().filter(target=request.user).order_by('-pk')[:10:1]
        active_jobs = Job.objects.all().filter(accepted=True).exclude(status__status_name="DN")
        completed_jobs = len(Job.objects.all().filter(status__status_name="DN"))
        translator_count = len(User.objects.all().filter(is_staff=True, is_active=True, is_superuser=False)) 
        pending_jobs = len(Job.objects.all().filter(paid=False))
        active_jobs_count = len(active_jobs)

        return render(request, 'administrator/admin_dashboard.html', {"dashboard":True, "notifications":notifications, "active_jobs":active_jobs, "completed_jobs":completed_jobs, "translator_count":translator_count, "pending_jobs":pending_jobs, "active_jobs_count":active_jobs_count})
    
    elif request.user.is_staff and request.user.is_active: #Translator
        translation_contracts = []
        proofreading_contracts = []
        transcribing_contracts = []
        interpretation_contracts = []
        profile_obj = Profile.objects.get(user=request.user)
        completed_contracts = Contract.objects.all().filter(profile=request.user, completed=True)
        total_earning = 0
        total_rating = 0
        total_rated_contracts = 0
        for contract in completed_contracts:
            total_earning += contract.contract_price
            if contract.rating:
                total_rating += contract.rating
                total_rated_contracts += 1
        try:
            avg_rating = int(total_rating//total_rated_contracts)
        except:
            avg_rating = 0
        stars = []
        for star in range(avg_rating):
            stars.append(star)
        ongoing_projects = Contract.objects.all().filter(profile=request.user, completed=False).count()
        for from_language in profile_obj.from_languages.all():
            for to_language in profile_obj.to_languages.all():
                print(from_language, to_language)
                translation_contracts.extend(Contract.objects.all().filter(status = "TR",dependency = None, is_signed=False, target_language=to_language, job__source_language = from_language, job__paid = True))
                proofreading_contracts.extend(Contract.objects.all().filter(status = "PR", dependency__completed = True, is_signed=False, target_language=to_language, job__source_language = from_language, job__paid = True))
                transcribing_contracts.extend(Contract.objects.all().filter(status = "TS", dependency = None, is_signed=False, target_language=to_language, job__source_language = from_language, job__paid = True))
                interpretation_contracts.extend(Contract.objects.all().filter(status= "IN",dependency = None, is_signed=False, target_language=to_language, job__source_language = from_language, job__paid = True))

        print(transcribing_contracts, interpretation_contracts)
        notifications = Notifications.objects.all().filter(target=request.user).order_by('-pk')[:10:1]
        return render(request, 'employee/translator_dashboard.html', {"dashboard":True, "notifications":notifications, "completed_contracts":len(completed_contracts), "translation_contracts":translation_contracts, "proofreading_contracts":proofreading_contracts, "transcribing_contracts":transcribing_contracts, "interpretation_contracts":interpretation_contracts,  "total_earning":total_earning, "ongoing_projects":ongoing_projects, "stars":stars})
    
    elif request.user.is_active: #customer
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
        notifications = Notifications.objects.all().filter(target=request.user).order_by('-pk')[:2:1]
        
        return render(request, 'customer/dashboard.html', {"notifications":notifications, "active_jobs":active_jobs, "draft_jobs":active_drafts, "completed_jobs":completed_jobs})
    else:
        return redirect("/login")       
            
def feedback(request, contract_id):
    if request.user.is_active:
        contract_obj = Contract.objects.get(contract_id=contract_id)
        return render(request, 'customer/feedback.html', {"contract_obj":contract_obj})
    else:
        return redirect("/login")  

def jobs_details(request, job_id):
    if request.user.is_active:
        job_obj = Job.objects.get(job_id=job_id)
        contracts = Contract.objects.all().filter(job=job_obj)

        return render(request, 'customer/jobs_details.html',{"job_obj":job_obj, "contracts":contracts})
    else:
        return redirect("/login")  