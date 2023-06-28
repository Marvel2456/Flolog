from django.db import models
from accounts.models import Client
import uuid

# Create your models here.



class Medication(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    owner = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='owner')
    generic_name = models.CharField(max_length=250, blank=True, null=True)
    brand_name = models.CharField(max_length=250, blank=True, null=True)

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
    dosage_form = models.CharField(max_length=20, choices=DOSAGE_CHOICES, default='TABLET', blank=True, null=True)
    dose_strength = models.CharField(max_length=150, blank=True, null=True)
    upload_prescription = models.FileField(upload_to='upload/prescription', blank=True, null=True)
    extra_info = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.generic_name)


class Order(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    owner = models.ForeignKey(Client, on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, on_delete=models.PROTECT)
    recipent_name = models.CharField(max_length=150, blank=True, null=True)
    recipent_phone_number = models.CharField(max_length=20, blank=True, null=True)
    recipent_address = models.CharField(max_length=250, blank=True, null=True)
    state = models.CharField(max_length=150, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)

    PENDING = 'PEN'
    DELIVERED = 'DEL'

    STATUS = [
        (PENDING, 'PEN'),
        (DELIVERED, 'DEL')
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='PEN')
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.owner.email

#  Link the order_medication with the order using another model called cart, so that to create an order, all we need is the cart_id, and then we will fill in the other details


