from django.shortcuts import render, redirect
from common.models import Language, Content
from profiles.models import Profile
from services.models import Contract, Job
# Create your views here.
def create_translator(request):
    if request.user.is_superuser and request.user.is_active:
        languages = Language.objects.all()
        content_types = Content.objects.all()
        return render(request, 'administrator/create_translator.html',{"languages":languages, "content_types":content_types})
    else:
        return redirect("/login") #TODO replace with view url lookups.   

def view_employee(request):
    if request.user.is_superuser and request.user.is_active:
        all_profiles = Profile.objects.all()
        return render(request, 'administrator/view_employee.html', {"all_profiles":all_profiles})
    else:
        return redirect("/login") #TODO replace with view url lookups.   


def available_jobs(request):
    if request.user.is_superuser and request.user.is_active:
       
        active_jobs = Job.objects.all().filter(accepted=True, paid=True)
        return render(request, 'administrator/available_jobs.html', {"active_jobs":active_jobs})
    else:
        return redirect("/login") #TODO replace with view url lookups.   


'''
def available_contracts(request, contract_id):
    if request.user.is_superuser and request.user.is_active:
        translation_contracts.extend(Contract.objects.all().filter(dependency = None, is_signed=False, job__paid = True))
        proofreading_contracts.extend(Contract.objects.all().filter(dependency__completed = True, is_signed=False, job__paid = True))
        return render(request, 'administrator/available_jobs_details.html')
    else:
        return redirect("/login") #TODO replace with view url lookups.   
'''

def available_jobs_details(request, job_id):
    if request.user.is_superuser and request.user.is_active:
        job_obj = Job.objects.get(job_id=job_id)
        contracts = Contract.objects.all().filter(job=job_obj)
        all_employees = Profile.objects.all().filter(title="TR")

        return render(request, 'administrator/available_jobs_details.html', {"contracts":contracts, "all_employees":all_employees})
    else:
        return redirect("/login") #TODO replace with view url lookups.   

def accepted_contracts(request):
    if request.user.is_superuser and request.user.is_active:
        accepted_contracts = Contract.objects.all().filter(is_signed=True, completed=False)
        print(accepted_contracts)
        return render(request, 'administrator/accepted_contracts.html', {"accepted_contracts":accepted_contracts})
    else:
        return redirect("/login") #TODO replace with view url lookups.   

def completed_contracts(request):
    if request.user.is_superuser and request.user.is_active:
        payment_completed = Contract.objects.all().filter(completed=True, paid=True)
        payment_due = Contract.objects.all().filter(completed=True, paid=False)

        return render(request, 'administrator/completed_contracts.html', {"payment_completed":payment_completed, "payment_due":payment_due})
    else:
        return redirect("/login") #TODO replace with view url lookups.   

def translator_completed_contracts_due(request, username):
    if request.user.is_superuser and request.user.is_active:
        from users.models import User
        if User.objects.filter(username=username).exists():
            user_obj = User.objects.get(username=username)
            completed_contracts_due = Contract.objects.all().filter(completed=True, paid=False, profile=user_obj)
            return render(request, 'administrator/completed_contracts_due.html', {"completed_contracts_due":completed_contracts_due, "username":user_obj.get_full_name()})
        else:
            return render(request, 'base/404.html')
    else:
        return redirect("/login") #TODO replace with view url lookups.   

def translator_completed_contracts_paid(request, username):
    if request.user.is_superuser and request.user.is_active:
        from users.models import User
        if User.objects.filter(username=username).exists():
            user_obj = User.objects.get(username=username)
            completed_contracts_paid = Contract.objects.all().filter(paid=True, profile=user_obj)
            return render(request, 'administrator/completed_contracts_paid.html', {"completed_contracts_paid":completed_contracts_paid, "username":user_obj.get_full_name()})
        else:
            return render(request, 'base/404.html')
    else:
        return redirect("/login") #TODO replace with view url lookups.   

def translator_completed_contracts_all(request, username):
    if request.user.is_superuser and request.user.is_active:
        from users.models import User
        if User.objects.filter(username=username).exists():
            user_obj = User.objects.get(username=username)
            completed_contracts_all = Contract.objects.all().filter(profile=user_obj)
            return render(request, 'administrator/translator_completed_contracts.html', {"completed_contracts_all":completed_contracts_all, "username":user_obj.get_full_name()})
        else:
            return render(request, 'base/404.html')
    else:
        return redirect("/login") #TODO replace with view url lookups.   



def translator_accepted_contracts(request, username):
    if request.user.is_superuser and request.user.is_active:
        from users.models import User
        if User.objects.filter(username=username).exists():
            user_obj = User.objects.get(username=username)
            accepted_contracts = Contract.objects.all().filter(is_signed=True, completed=False, profile=user_obj)
            return render(request, 'administrator/translator_accepted_contracts.html', {"accepted_contracts":accepted_contracts, "username":user_obj.get_full_name()})
        else:
            return render(request, 'base/404.html')
    else:
        return redirect("/login") #TODO replace with view url lookups.   




def view_employee_details(request, username):
    if request.user.is_superuser and request.user.is_active:
        from users.models import User
        if User.objects.filter(username=username).exists():
            user_obj = User.objects.get(username=username)
            profile_obj = Profile.objects.get(user=user_obj)
            return render(request, 'administrator/view_employee_details.html', {"profile_obj":profile_obj})
        else:
            return render(request, 'base/404.html')
    else:
        return redirect("/login") #TODO replace with view url lookups.

def edit_employee(request):
    if request.user.is_superuser and request.user.is_active:
        return render(request, 'administrator/edit_employee.html')
        
    else:
        return redirect("/login")   
