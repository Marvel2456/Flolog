from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(MedicalRecord)
admin.site.register(MedicalHistory)
admin.site.register(Allergy)
admin.site.register(FamilyHistory)
admin.site.register(Age)
admin.site.register(History)
admin.site.register(RiskFactor)
admin.site.register(PatientAllergy)
