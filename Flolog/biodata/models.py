from django.db import models
from accounts.models import ClientProfile
import uuid

# Create your models here.
class MedicalRecord(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    owner = models.OneToOneField(ClientProfile, on_delete=models.PROTECT, blank=True, null=True)
    Sex_choice = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    sex = models.CharField(max_length=20, choices=Sex_choice, default="Male", blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    weight = models.PositiveIntegerField(blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)
    Blood_Group_Chpice = (
        ('O', 'O'),
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
    )
    blood_group = models.CharField(max_length=10, choices=Blood_Group_Chpice, default="O", blank=True, null=True)
    Genotype_Choice = (
        ('AA', 'AA'),
        ('AS', 'AS'),
        ('AC', 'AC'),
        ('SS', 'SS'),
        ('SC', 'SC'),
    )
    genotype = models.CharField(max_length=10, choices=Genotype_Choice, default="AA", blank=True, null=True)

    def __str__(self):
        return self.owner.email
    

class Allergy(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    owner = models.ForeignKey(ClientProfile, on_delete=models.PROTECT, blank=True, null=True)
    allergy_name = models.CharField(max_length=200, blank=True, null=True)
    symptom = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "allergies"

    def __str__(self):
        return self.owner.email


class MedicalHistory(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    owner = models.ForeignKey(ClientProfile, on_delete=models.PROTECT, blank=True, null=True)
    medical_history_name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.owner.email

class FamilyHistory(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    owner = models.ForeignKey(ClientProfile, on_delete=models.PROTECT, blank=True, null=True)
    relationship = models.CharField(max_length=200, blank=True, null=True)
    details = models.CharField(max_length=250, blank=True, null=True)
    risk_factor = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.owner.email
    