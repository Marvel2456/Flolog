from rest_framework import serializers
from .models import *
from accounts.serializers import *
from accounts.models import CustomUser
from biodata.serializers import MedicalHistorySerializer, MedicalRecordSerializer, PatientAllergySerialier, FamilyHistorySerializer
from accounts.serializers import ClientSerializer

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

# class MessageSerializer(serializers.ModelSerializer):
#     # sender = CustomUserSerializer()

#     class Meta:
#         model = Message
#         fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.EmailField(source='sender.user.email', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'room', 'sender_email', 'content', 'timestamp']


class ChatroomSerializer(serializers.ModelSerializer):
    client_email = serializers.EmailField(source='client.user.email', read_only=True)
    pharmacist_email = serializers.EmailField(source='pharmacist.user.email', read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    med_records = MedicalRecordSerializer(read_only=True)
    med_history = MedicalHistorySerializer(read_only=True)
    fam_history = FamilyHistorySerializer(read_only=True)
    allergy = PatientAllergySerialier(read_only=True)

    class Meta:
        model = Chatroom
        fields = ['id', 'channel_name', 'client_email', 'pharmacist_email', 'is_active', 'end_time', 'messages', 'med_records', 'med_history', 'fam_history', 'allergy']

# class ChatroomSerializer(serializers.ModelSerializer):
#     messages = MessageSerializer(many=True, read_only=True)

#     class Meta:
#         model = Chatroom
#         fields = '__all__'

