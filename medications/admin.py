from django.contrib import admin
from .models import Order, Medication

# Register your models here.
admin.site.register(Order)
admin.site.register(Medication)