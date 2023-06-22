from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import CustomUser, Client, Pharmacist
from .models import MedicalRecord, MedicalHistory, PatientAllergy, FamilyHistory


@receiver(post_save, sender=Client)
def create_medical_record(sender, instance, created, **kwargs):
    client = CustomUser.objects.filter(is_client=True)
    if created:
        
        client = instance
        if instance:
            medical_record = MedicalRecord.objects.create(
                owner = client,
                
            )

@receiver(post_save, sender=CustomUser)
def create_medical_history(sender, instance, created, **kwargs):
    # client = CustomUser.objects.filter(is_client=True)
    if created:
        
        user = instance
        if instance.is_client:
            medical_history = MedicalHistory.objects.create(
                owner = user,
                
            )

@receiver(post_save, sender=CustomUser)
def create_patient_allergy(sender, instance, created, **kwargs):
    # client = CustomUser.objects.filter(is_client=True)
    if created:
        
        user = instance
        if instance.is_client:
            patient_allergy = PatientAllergy.objects.create(
                owner = user,
                
            )

@receiver(post_save, sender=CustomUser)
def create_family_history(sender, instance, created, **kwargs):
    # client = CustomUser.objects.filter(is_client=True)
    if created:
        
        user = instance
        if instance.is_client:
            family_history = FamilyHistory.objects.create(
                owner = user,
                
            )