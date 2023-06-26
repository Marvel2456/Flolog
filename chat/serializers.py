from rest_framework import serializers
from .models import *
from accounts.serializers import *
from accounts.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    # sender = CustomUserSerializer()

    class Meta:
        model = Message
        fields = '__all__'


class ChatroomSerializer(serializers.ModelSerializer):
    client_email = serializers.EmailField(source='client.user.email', read_only=True)
    pharmacist_email = serializers.EmailField(source='pharmacist.user.email', read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Chatroom
        fields = ['id', 'client_email', 'pharmacist_email', 'is_active', 'end_time', 'messages']

# class ChatroomSerializer(serializers.ModelSerializer):
#     messages = MessageSerializer(many=True, read_only=True)

#     class Meta:
#         model = Chatroom
#         fields = '__all__'

