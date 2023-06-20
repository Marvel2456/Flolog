from rest_framework import serializers
from .models import *
from accounts.serializers import *
from accounts.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'



class ChatroomSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    pharmacist = PharmacistSerializer()

    class Meta:
        model = Chatroom
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    sender = CustomUserSerializer()

    class Meta:
        model = Message
        fields = '__all__'
