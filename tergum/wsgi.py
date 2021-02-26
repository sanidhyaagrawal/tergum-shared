"""
WSGI config for tergum project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

"""os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tergum.settings')"""
settings_module = "tergum.production" if 'WEBSITE_HOSTNAME' in os.environ else 'tergum.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)


application = get_wsgi_application()
