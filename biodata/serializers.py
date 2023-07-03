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


class PatientAllergySerializer(serializers.ModelSerializer):
    allergy = AllergySerializer(many=True, source='allergies')
    owner = ClientSerializer(many=False, read_only=True)
    class Meta:
        model = PatientAllergy
        fields = '__all__'


    # def create(self, validated_data):
    #     allergies_data = validated_data.pop('allergies')
    #     patient_allergy = PatientAllergy.objects.create()

    #     for allergy_data in allergies_data:
    #         allergy, _ = Allergy.objects.get_or_create(**allergy_data)
    #         patient_allergy.allergies.add(allergy)

    #     return patient_allergy
    
class MedicalHistorySerializer(serializers.ModelSerializer):
    history = HistorySerializer(many=True)
    owner = ClientSerializer(many=False, read_only=True)
    class Meta:
        model = MedicalHistory
        fields = '__all__'

    def create(self, validated_data):
        histories_data = validated_data.pop('histories')
        med_history = MedicalHistory.objects.create()

        for history_data in histories_data:
            history, _ = History.objects.get_or_create(**history_data)
            med_history.histories.add(history)

        return med_history

class FamilyHistorySerializer(serializers.ModelSerializer):
    risk = RiskFactorSerializer(many=True)
    owner = ClientSerializer(many=False, read_only=True)
    class Meta:
        model = FamilyHistory
        fields = '__all__'

    def create(self, validated_data):
        risks_data = validated_data.pop('risks')
        fam_history = FamilyHistory.objects.create()

        for risk_data in risks_data:
            risk_factor, _ = RiskFactor.objects.get_or_create(**risk_data)
            fam_history.risks.add(risk_factor)

        return fam_history


class AdminMedicalRecordSerializer(serializers.ModelSerializer):
    owner = ClientSerializer(read_only=True)
    class Meta:
        model = MedicalRecord
        fields = ['id', 'owner', 'sex', 'age', 'weight', 'height', 'blood_group', 'genotype',]


class AdminAllergySerializer(serializers.ModelSerializer):
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



