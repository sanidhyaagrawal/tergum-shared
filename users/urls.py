from django.urls import path

from . import views
from . import apis

app_name = 'common'
#Conatins views for User model related tasks  
#like signup, log-in, change password, etc.

urlpatterns = [
    #GET requests
    path('login', views.login, name='login'), #retuns login page
    path('logout', views.logout_view, name='logout'), #logs out user, redirects to home page
    path('signup', views.signup, name='signup'), #returns sign-up account page
    path('user/account/revocery/<str:token>', views.recovery, name='recovery'), #returns sign-up account page


    #apis
    path('api/user/account/revocery', apis.forget_password, name='forget_password'), #returns sign-up account page
    path('api/user/account/recover', apis.recover_password, name='recover_password'), #returns sign-up account page
    
    path('login_api', apis.login_api, name='login_api'), #POST | API to login
    path('signup_api', apis.signup_api, name='signup_api'), #POST | API to create an account
]

