from django.contrib import admin
from .models import Order, OrderMedication

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderMedication)