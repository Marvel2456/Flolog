from rest_framework import serializers
from .models import *
from accounts.serializers import ClientSerializer


class MedicalRecordSerializer(serializers.ModelSerializer):
    owner = ClientSerializer(many=False, read_only=True)
    class Meta:
        model = MedicalRecord
        fields = ['owner', 'sex', 'age', 'weight', 'height', 'blood_group', 'genotype',]


class AllergySerialier(serializers.ModelSerializer):
    owner = ClientSerializer(many=False, read_only=True)
    class Meta:
        model = Allergy
        fields = ['owner', 'allergy_name', 'symptom',]

class MedicalHistorySerializer(serializers.ModelSerializer):
    owner = ClientSerializer(many=False, read_only=True)
    class Meta:
        model = MedicalHistory
        fields = ['owner', 'medical_history_name',]


class FamilyHistorySerializer(serializers.ModelSerializer):
    owner = ClientSerializer(many=False, read_only=True)
    class Meta:
        model = FamilyHistory
        fields = ['owner', 'relationship', 'details', 'risk_factor',]


class AdminMedicalRecordSerializer(serializers.ModelSerializer):
    owner = ClientSerializer(read_only=True)
    class Meta:
        model = MedicalRecord
        fields = ['id', 'owner', 'sex', 'age', 'weight', 'height', 'blood_group', 'genotype',]


class AdminAllergySerialier(serializers.ModelSerializer):
    owner = ClientSerializer()
    class Meta:
        model = Allergy
        fields = ['id', 'owner', 'allergy_name', 'symptom',]


class AdminMedicalHistorySerializer(serializers.ModelSerializer):
    owner = ClientSerializer()
    class Meta:
        model = MedicalHistory
        fields = ['id', 'owner', 'medical_history_name',]


class AdminFamilyHistorySerializer(serializers.ModelSerializer):
    owner = ClientSerializer()
    class Meta:
        model = FamilyHistory
        fields = ['owner', 'relationship', 'details', 'risk_factor',]



