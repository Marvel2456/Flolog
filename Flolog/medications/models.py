from django.db import models
from accounts.models import ClientProfile
import uuid

# Create your models here.




class Order(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    owner = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
    recipent_name = models.CharField(max_length=150, blank=True, null=True)
    recipent_phone_number = models.CharField(max_length=20, blank=True, null=True)
    recipent_address = models.CharField(max_length=250, blank=True, null=True)
    state = models.CharField(max_length=150, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.owner



class OrderMedication(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True) 
    generic_name = models.CharField(max_length=250, blank=True, null=True)
    brand_name = models.CharField(max_length=250, blank=True, null=True)
    dosage = models.CharField(max_length=100, blank=True, null=True)
    dose_strength = models.CharField(max_length=150, blank=True, null=True)
    upload_prescription = models.FileField(upload_to='upload/prescription', blank=True, null=True)
    extra_info = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order.owner