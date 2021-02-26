
from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import *
from services.models import *
from common.models import *
# from employees.models import *
from profiles.models import *
from users.models import *

# Register your models here.
admin.site.register(Content)
admin.site.register(Status)
admin.site.register(JobType)
admin.site.register(Language)
admin.site.register(Quality)
admin.site.register(Rate)
admin.site.register(Attachment)
admin.site.register(Contract)
admin.site.register(Company)
# admin.site.register(Employee)
admin.site.register(Variables)

#admin.site.register(Skill)
admin.site.register(User)
class UserAdmin(UserAdmin):
    readonly_fields = [
        'date_joined',
    ]
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()  # type: Set[str]

        if not is_superuser:
            disabled_fields |= {
                'username',
                'is_superuser',
                'user_permissions',
            }

        # Prevent non-superusers from editing their own permissions
        if (
            not is_superuser
            and obj is not None
            and obj == request.user
        ):
            disabled_fields |= {
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form

        actions = [
        'activate_users',
    ]

    def activate_users(self, request, queryset):
        assert request.user.has_perm('auth.change_user')
        cnt = queryset.filter(is_active=False).update(is_active=True)
        self.message_user(request, 'Activated {} users.'.format(cnt))
    activate_users.short_description = 'Activate Users'  # type: ignore

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm('auth.change_user'):
            del actions['activate_users']
        return actions
        
admin.site.register(Profile)
