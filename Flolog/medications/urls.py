from django.urls import path
from .views import *


#  Write your urls here

urlpatterns = [
    path("order/", OrderView.as_view(), name="order"),
    path("medication/", MedicationView.as_view(), name="medication"),
    path("admin_order/", AdminOrderView.as_view(), name="admin_order"),
    path("admin_medication/", AdminMedicationView.as_view(), name="admin_medication")
]
