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


from users.apis import validatePassToken

def recovery(request, token):
    """
    log-out user's session.   
    """
    if request.user.is_active:
        return redirect("/dashboard") 
    else:
        is_valid, reason, obj = validatePassToken(token)
        if is_valid:
            return render(request, 'users/first_time_password_reset.html', {"token":token})
        else:
            return render(request, 'users/link_expired.html', {"reason": reason})

