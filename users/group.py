import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_permission.settings')

import django

django.setup()
from django.contrib.auth.models import Group


GROUPS = ['translator', 'editor','manager','secretary']
MODELS = ['user']

#create groups if not alredy exist as soon as server run.
for group in GROUPS:
    new_group, created = Group.objects.get_or_create(name=group)