from django.contrib import admin
from django.contrib.admin import ModelAdmin, site
from .models import *



#config on how to diplay Job model in Django's admin pannel
class JobModelAdmin(admin.ModelAdmin):
    readonly_fields = ('posted_date',)
    list_display = ('job_id', 'paid', 'employeer', 'source_language', 'get_number_of_target_languages', 'posted_date', 'calculate_total_price')
    list_filter = ('paid',)

# Register your models here.
admin.site.register(Job, JobModelAdmin)
