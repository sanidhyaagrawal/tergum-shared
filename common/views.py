
from django.shortcuts import render, redirect

def index(request): #URI --> <domain_name>
    """
    Redirects to dashboard if the user is authenticated, 
    otherwise renders the landing page.    
    """
    ISO = request.LANGUAGE_CODE

    if request.user.is_active:
        
        #user is authenticated
        return redirect("/dashboard")
    else:
        if ISO == "ar":
            return render(request, 'common/homescreen_ar.html')
        else:
            return render(request, 'common/homescreen.html')

'''
def amharic(request): #URI --> <domain_name>
    """
    Redirects to dashboard if the user is authenticated, 
    otherwise renders the landing page.    
    """
'''