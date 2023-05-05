from django.contrib import admin
from .models import CustomUser, ClientProfile, PharmacistProfile, Plan

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(ClientProfile)
admin.site.register(PharmacistProfile)
admin.site.register(Plan)