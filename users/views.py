from django.shortcuts import render, redirect
from django.contrib.auth import logout

def login(request): 
    """
    Render frontend for login screen, 
    redirects to dashboard if request is alredy authenticated.   
    """
    if request.user.is_active:
        return redirect("/dashboard") 
    else:
        return render(request, 'users/login.html')

def signup(request):
    """
    Render frontend for signup screen
    redirects to dashboard if request is alredy authorized.      
    """
    if request.user.is_active:
        return redirect("/dashboard") 
    else:
        return render(request, 'users/signup.html')

def logout_view(request):
    """
    log-out user's session.   
    """
    if request.user.is_active:
        logout(request)
    return redirect("/") #redirect to home screen after log-out       