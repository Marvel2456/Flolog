from django.urls import path
from .views import *


urlpatterns = [
    path('age/', AgeView.as_view(), name='age'),
    path('allergy/', AllergyView.as_view(), name='allergy'),
    path('history/', HistoryView.as_view(), name='history'),
    path('risk/', RiskFactorView.as_view(), name='risk'),
    path("record/", MedicalRecordView.as_view(), name="record"),
    path("record_detail/<str:uuid>/", MedicalRecordDetailView.as_view(), name="record_detail"),
    path("patient_history/", MedicalHistoryView.as_view(), name="patient_history"),
    path("history_detail/<str:uuid>/", MedicalHistoryDetailView.as_view(), name="history_detail"),
    path("pateint_allergy/", PatientAllergyView.as_view(), name="patient_allergy"),
    path("allergy_detail/<str:uuid>/", AllergyDetailView.as_view(), name="allergy_detail"),
    path("family/", FamilyHistoryView.as_view(), name="family"),
    path("family_detail/<str:uuid>/", FamilyHistoryDetailView.as_view(), name="family_detail"),
    path("admin_record/", AdminMedicalRecordView.as_view(), name="admin_record"),
    path('admin_record_detail/<str:uuid>/', AdminMedicalRecordDetailView.as_view(), name="admin_record_detail"),
    path("admin_history/", AdminMedicalHistoryView.as_view(), name="admin_history"),
    path("admin_history_detail/<str:uuid>/", AdminMedicalHistoryDetailView.as_view(), name="admin_history_detail"),
    path("admin_allergy/", AdminAllergyView.as_view(), name="admin_allergy"),
    path("admin_allergy_detail/<str:uuid>/", AdminAllergyDetailView.as_view(), name="admin_allergy_detail"),
    path("admin_family/", AdminFamilyHistoryView.as_view(), name="admin_family"),
    path("admin_family_detail/<str:uuid>/", AdminFamilyHistoryDetailView.as_view(), name="admin_family_detail"),
]

# Write signals for the pharmacist to be able to edit client biodata