from django.db import models
from accounts.models import CustomUser
import uuid

# Create your models here.


class Medication(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='owner')
    upload_prescription = models.FileField(upload_to='upload/prescription', blank=True, null=True)
    medication_details = models.JSONField(default=list)
    recipent_name = models.CharField(max_length=150, blank=True, null=True)
    recipent_phone_number = models.CharField(max_length=20, blank=True, null=True)
    recipent_address = models.CharField(max_length=250, blank=True, null=True)
    state = models.CharField(max_length=150, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    STATUS = [
        ('PENDING', 'PENDING'),
        ('DELIVERED', 'DELIVERED')
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='PENDING')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f'{self.recipent_name} - {self.owner}')
    

class MedicationDetail(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE, related_name='details')
    DOSAGE_CHOICES = [
        ('TABLET', 'TABLET'),
        ('CAPSULE', 'CAPSULE'),
        ('SYRUP', 'SYRUP'),
        ('SOLUTION', 'SOLUTION'),
        ('EMULSION', 'EMULSION'),
        ('SUSPENSION', 'SUSPENSION'),
        ('INHALER', 'INHALER'),
        ('CREAM', 'CREAM'),
        ('PASTE', 'PASTE'),
        ('GEL', 'GEL'),
    ]
    generic_name = models.CharField(max_length=250, blank=True, null=True)
    brand_name = models.CharField(max_length=250, blank=True, null=True)
    dosage_form = models.CharField(max_length=20, choices=DOSAGE_CHOICES, default='TABLET', blank=True, null=True)
    dose_strength = models.CharField(max_length=150, blank=True, null=True)
    extra_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.generic_name
