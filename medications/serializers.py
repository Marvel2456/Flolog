from rest_framework import serializers
from .models import Order, Medication
from accounts.serializers import ClientSerializer


class AdminMedicationSerializer(serializers.ModelSerializer):
    owner = ClientSerializer()
    class Meta:
        model = Medication
        fields = ['owner', 'generic_name', 'brand_name', 'dosage_form', 'dose_strength', 'extra_info', 'upload_prescription',]

class AdminOrderSerializer(serializers.ModelSerializer):
    owner = ClientSerializer()
    class Meta:
        model = Order
        fields = ['owner', 'medication', 'recipent_name', 'recipent_phone_number', 'recipent_address', 'state', 'city', 'status',]


class MedicationSerializer(serializers.ModelSerializer):
    owner = ClientSerializer(many=False, read_only=True)
    class Meta:
        model = Medication
        fields = ['generic_name', 'brand_name', 'dosage_form', 'dose_strength', 'extra_info', 'upload_prescription', 'owner']


class OrderSerializer(serializers.ModelSerializer):
    owner = ClientSerializer(many=False, read_only=True)
    medication = MedicationSerializer(many=True) 
    class Meta:
        model = Order
        fields = ['medication', 'recipent_name', 'recipent_phone_number', 'recipent_address', 'state', 'city', 'owner']

