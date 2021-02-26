from django.contrib import admin
from django.contrib.admin import ModelAdmin, site
from .models import *

# Register your models here.


site.register(stripe_keys)
site.register(payment_tokens)
