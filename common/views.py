
from django.shortcuts import render, redirect

def index(request): #URI --> <domain_name>
    """
    Redirects to dashboard if the user is authenticated, 
    otherwise renders the landing page.    
    """
    if request.user.is_active:
        #user is authenticated
        return redirect("/dashboard")
    else:
        return render(request, 'common/homescreen.html')

