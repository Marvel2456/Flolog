from django.urls import path
from .views import *


#  Write your urls here

urlpatterns = [
    # path("order/", OrderView.as_view(), name="order"),
    path("medication/", MedicationView.as_view(), name="medication"),
    # Test the endpoints below
    # path("admin_order/", AdminOrderView.as_view(), name="admin_order"),
    path("admin_medication/", AdminMedicationView.as_view(), name="admin_medication"),
    # path("order_details/<str:uuid>/", OrderDetailView.as_view(), name="order_details"),
    path("medication_details/<str:uuid>/", MedicationDetailView.as_view(), name="medication_details"),
    # path("admin_order_details/<str:uuid>/", AdminOrderDetailView.as_view(), name="admin_order_details"),
    path("admin_medication_details/<str:uuid>/", AdminMedicationDetailView.as_view(), name="admin_medication_details"),
    
]
