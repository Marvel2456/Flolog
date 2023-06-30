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

    # def create(self, validated_data):
    #     allergies_data = validated_data.pop('allergy')
    #     patient_allergy = PatientAllergy.objects.create(**validated_data)

    #     for allergy_data in allergies_data:
    #         allergy = Allergy.objects.get(id=allergy_data['id'])
    #         patient_allergy.allergy.add(allergy)

    #     patient_allergy.save()
    #     return patient_allergy

    # def update(self, instance, validated_data):
    #     allergies_data = validated_data.pop('allergy')

    #     instance.allergy.clear()
    #     for allergy_data in allergies_data:
    #         allergy = Allergy.objects.get(id=allergy_data['id'])
    #         instance.allergy.add(allergy)

    #     instance.others = validated_data.get('others', instance.others)
    #     instance.save()
    #     return instance
        
    
class MedicalHistorySerializer(serializers.ModelSerializer):
    history = HistorySerializer(many=True)
    owner = ClientSerializer(many=False, read_only=True)
    class Meta:
        model = MedicalHistory
        fields = ['owner', 'history', 'others',]

    # def create(self, validated_data):
    #     histories_data = validated_data.pop('history')
    #     med_history = MedicalHistory.objects.create(**validated_data)

    #     for history_data in histories_data:
    #         history = History.objects.get(id=history_data['id'])
    #         med_history.history.add(history)

    #     med_history.save()
    #     return med_history

    # def update(self, instance, validated_data):
    #     histories_data = validated_data.pop('history')

    #     instance.history.clear()
    #     for history_data in histories_data:
    #         history = History.objects.get(id=history_data['id'])
    #         instance.history.add(history)

    #     instance.others = validated_data.get('others', instance.others)
    #     instance.save()
    #     return instance


class FamilyHistorySerializer(serializers.ModelSerializer):
    risk = RiskFactorSerializer(many=True)
    owner = ClientSerializer(many=False, read_only=True)
    class Meta:
        model = FamilyHistory
        fields = ['owner', 'risk', 'others',]

    # def create(self, validated_data):
    #     risks_data = validated_data.pop('risk')
    #     fam_history = FamilyHistory.objects.create(**validated_data)

    #     for risk_data in risks_data:
    #         risk = RiskFactor.objects.get(id=risk_data['id'])
    #         fam_history.risk.add(risk)

    #     fam_history.save()
    #     return fam_history

    # def update(self, instance, validated_data):
    #     risks_data = validated_data.pop('risk')

    #     instance.history.clear()
    #     for risk_data in risks_data:
    #         risk = RiskFactor.objects.get(id=risk_data['id'])
    #         instance.risk.add(risk)

    #     instance.others = validated_data.get('others', instance.others)
    #     instance.save()
    #     return instance


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



