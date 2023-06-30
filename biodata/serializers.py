from rest_framework import serializers
from .models import *
from accounts.serializers import ClientSerializer


class AgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Age
        fields = '__all__'


class AllergySerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergy
        fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'

class RiskFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskFactor
        fields = '__all__'


class MedicalRecordSerializer(serializers.ModelSerializer):
    owner = ClientSerializer(many=False, read_only=True)
    class Meta:
        model = MedicalRecord
        fields = ['owner', 'sex', 'age', 'weight', 'height', 'blood_group', 'genotype',]


class PatientAllergySerialier(serializers.ModelSerializer):
    allergy = AllergySerializer(many=True)
    owner = ClientSerializer(many=False, read_only=True)
    class Meta:
        model = PatientAllergy
        fields = ['owner', 'allergy', 'others',]
    
class MedicalHistorySerializer(serializers.ModelSerializer):
    history = HistorySerializer(many=True)
    owner = ClientSerializer(many=False, read_only=True)
    class Meta:
        model = MedicalHistory
        fields = ['owner', 'history', 'others',]


class FamilyHistorySerializer(serializers.ModelSerializer):
    risk = RiskFactorSerializer(many=True)
    owner = ClientSerializer(many=False, read_only=True)
    class Meta:
        model = FamilyHistory
        fields = ['owner', 'risk', 'others',]


class AdminMedicalRecordSerializer(serializers.ModelSerializer):
    owner = ClientSerializer(read_only=True)
    class Meta:
        model = MedicalRecord
        fields = ['id', 'owner', 'sex', 'age', 'weight', 'height', 'blood_group', 'genotype',]


class AdminAllergySerialier(serializers.ModelSerializer):
    owner = ClientSerializer()
    class Meta:
        model = Allergy
        fields = ['id', 'owner', 'allergy', 'others',]


class AdminMedicalHistorySerializer(serializers.ModelSerializer):
    owner = ClientSerializer()
    class Meta:
        model = MedicalHistory
        fields = ['id', 'owner', 'history', 'others',]


class AdminFamilyHistorySerializer(serializers.ModelSerializer):
    owner = ClientSerializer()
    class Meta:
        model = FamilyHistory
        fields = ['owner', 'risk', 'others',]



