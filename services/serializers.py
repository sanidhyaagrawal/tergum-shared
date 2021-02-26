from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *

class attachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ('attachment_id', 'file', 'orignal_filename', 'word_count')
