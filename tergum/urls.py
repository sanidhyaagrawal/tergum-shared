
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls), #URL's for Django's admin pannel
    path('accounts/', include('allauth.urls')), #URLs for djngo-allauth (sign0in with google)
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #for localhost only.

#i18n_patterns URLs are once that start with ISO codes for internationalization
#like domain_name/en/... for english version, etc.
urlpatterns += i18n_patterns(
    path('', include('users.urls', namespace='users')),
    path('', include('profiles.urls', namespace='profiles')),
    path('', include('services.urls', namespace='services')),
    path('', include('common.urls', namespace='common')),  
    path('', include('payment_gateway.urls', namespace='payment_gateway')),  
    path('', include('administrator.urls', namespace='administrator')),  
    path('', include('employee.urls', namespace='employee')),  
)

