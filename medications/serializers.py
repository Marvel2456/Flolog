from rest_framework import serializers
from .models import Medication, MedicationDetail
from accounts.serializers import ClientSerializer


class AdminMedicationSerializer(serializers.ModelSerializer):
    owner = ClientSerializer()
    class Meta:
        model = Medication
        fields = [
            'id', 'owner', 'upload_prescription', 'medication_details', 'recipent_name', 
            'recipent_phone_number', 'recipent_address', 'state', 'city', 'status', 'created'
            ]


class MedicationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicationDetail
        fields = '__all__'

class MedicationSerializer(serializers.ModelSerializer):
    medication_details = MedicationDetailSerializer(many=True)

    class Meta:
        model = Medication
        fields = [
            'id', 'owner', 'upload_prescription', 'medication_details', 'recipent_name', 
            'recipent_phone_number', 'recipent_address', 'state', 'city', 'status', 'created'
            ]

    def create(self, validated_data):
        medication_details_data = validated_data.pop('medication_details')
        medication = Medication.objects.create(**validated_data)

        for detail_data in medication_details_data:
            MedicationDetail.objects.create(medication=medication, **detail_data)

        return medication

