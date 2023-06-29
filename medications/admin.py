from django.contrib import admin
from .models import  Medication, MedicationDetail

# Register your models here.
admin.site.register(MedicationDetail)
admin.site.register(Medication)