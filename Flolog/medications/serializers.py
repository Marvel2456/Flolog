from rest_framework import serializers
from .models import Medication, MedicationDetail
from accounts.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class AdminMedicationSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
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

    def create(self, validated_data):
        medication_details_data = validated_data.pop('medication_details')
        medication = Medication.objects.create(**validated_data)

        medication_details = []
        for med_detail in medication_details_data:
            med_detail = MedicationDetail(medication=medication, **med_detail)
            medication_details.append(med_detail)

        MedicationDetail.objects.bulk_create(medication_details)

        # Serialize the children objects
        serialized_medication_details = MedicationDetailSerializer(medication_details, many=True).data

        # Add the serialized children to the response
        medication_data = self.data
        medication_data['medication_details'] = serialized_medication_details

        return medication_data

    class Meta:
        model = Medication
        fields = [
            'id', 'owner', 'upload_prescription', 'medication_details', 'recipent_name', 
            'recipent_phone_number', 'recipent_address', 'state', 'city', 'status', 'created'
        ]