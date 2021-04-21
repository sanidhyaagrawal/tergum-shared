from django.contrib import admin
from django.contrib.admin import ModelAdmin, site
from .models import *

site.register(stripe_keys)
site.register(payment_tokens)
