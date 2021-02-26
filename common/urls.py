from django.urls import path

from . import views

app_name = 'common'
#Contains views for sceens that will be same for
#all users, like landing page or privacy polices. 

urlpatterns = [
    path('', views.index, name='index'), #landing page of the site
]