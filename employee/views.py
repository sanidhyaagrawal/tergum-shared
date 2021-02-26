from django.shortcuts import render, redirect

# Create your views here.
from services.models import Contract
def accepted_contracts(request):
    if request.user.is_staff and request.user.is_active:
        accepted_contracts = Contract.objects.all().filter(profile=request.user, completed=False)
        return render(request, 'employee/accepted_contracts.html', {"accepted_contracts":accepted_contracts})
    else:
        return redirect("/login") #TODO replace with view url lookups.      

def completed_contracts(request):
    if request.user.is_staff and request.user.is_active:
        completed_contracts = Contract.objects.all().filter(profile=request.user, completed=True)
        return render(request, 'employee/completed_contracts.html', {"completed_contracts": completed_contracts})
    else:
        return redirect("/login") #TODO replace with view url lookups.      

from profiles.models import Profile
def settings(request):
    if request.user.is_staff and request.user.is_active:
        profile = Profile.objects.get(user=request.user)
        return render(request, 'employee/settings.html', {"profile":profile})
    else:
        return redirect("/login") #TODO replace with view url lookups.      


'''          
def accepted_contracts_details(request, job_id):
    if request.user.is_staff and request.user.is_active:
        return render(request, 'employee/accepted_contracts_details.html')
    else:
        return redirect("/login") #TODO replace with view url lookups.      
            
            
def completed_contracts_details(request, job_id):
    if request.user.is_staff and request.user.is_active:
        return render(request, 'employee/completed_contracts_details.html')
    else:
        return redirect("/login") #TODO replace with view url lookups.      
'''

from services.verifiers import contract_id_is_valid       
def contract_details(request, contract_id):
    if request.user.is_staff and request.user.is_active:
        is_vaild, contract_obj = contract_id_is_valid(contract_id)
        if  is_vaild:
            if contract_obj.is_signed and contract_obj.profile == request.user or request.user.is_superuser:
                #if contract_obj.completed:

                    #return render(request, 'employee/completed_contracts_details.html', {"contract":contract_obj})
                #else:
                if contract_obj.dependency and contract_obj.dependency.completed ==  False:
                    return render(request, 'employee/500_translation_incomplete.html', {"contract_obj":contract_obj})
                else:
                    return render(request, 'employee/accepted_contracts_details.html', {"contract":contract_obj})
            else:
                return render(request, 'employee/500_contract_unauthorised.html', {"contract_id":contract_id})
        else:
            return render(request, 'base/404.html', {"contract_id":contract_id})
    else:
        return redirect("/login") #TODO replace with view url lookups.      
      
            
def invite_link_expired(request):
    return render(request, 'employee/link_expired.html')
  

from users.models import User
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login
from administrator.models import invite_links
def invite_link(request, email, token):
    print(email, token)
    if User.objects.all().filter(email=email.strip()).exists():
        user_obj = User.objects.get(email=email.strip())
    if invite_links.objects.all().filter(user=user_obj, token=token).exists():
        link_obj = invite_links.objects.get(user=user_obj, token=token)
        if user_obj.is_active == False:
            return render(request, 'employee/first_time_password_reset.html', {"token":token, "email":email})
        else:
            return render(request, 'employee/link_expired.html')
    else:
        return render(request, 'employee/link_expired.html')




