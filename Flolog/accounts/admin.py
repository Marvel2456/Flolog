from django.contrib import admin
from .models import CustomUser, Client, Pharmacist, Plan, Wallet

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Client)
admin.site.register(Pharmacist)
admin.site.register(Plan)
admin.site.register(Wallet)
