from rest_framework import serializers
from .models import *
from accounts.serializers import *
from accounts.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    sender = CustomUserSerializer()

    class Meta:
        model = Message
        fields = '__all__'

class ChatroomSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Chatroom
        fields = '__all__'

