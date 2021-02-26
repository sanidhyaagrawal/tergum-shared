from django.contrib.auth.models import User, Group
from rest_framework import serializers
from services.models import Message, Job
from users.models import User




class messageSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    class Meta:
        model = Message
        fields = ('text', 'employee', 'username')
