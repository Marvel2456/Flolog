from django.urls import path
from .views import *


#  Write your urls here

urlpatterns = [
    path("medication/", MedicationCreateAPIView.as_view(), name="medication"),
    # Test the endpoints below
    # path("admin_order/", AdminOrderView.as_view(), name="admin_order"),
    path("admin_medication/", AdminMedicationView.as_view(), name="admin_medication"),
    path("admin_medication_details/<str:uuid>/", AdminMedicationDetailView.as_view(), name="admin_medication_details"),
    
]
