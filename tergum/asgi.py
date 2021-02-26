"""
ASGI config for tergum project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

"""os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tergum.settings')"""
settings_module = "tergum.production" if 'WEBSITE_HOSTNAME' in os.environ else 'tergum.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
application = get_asgi_application()
