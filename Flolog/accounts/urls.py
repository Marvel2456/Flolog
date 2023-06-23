from django.urls import path, include
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)
from .views import *
from . import views



urlpatterns = [ 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register_client/', ClientRegisterView.as_view(), name="register_client" ),
    path('register_pharma/', PharmacistRegisterView.as_view(), name="register_pharma" ),
    path('login/', LoginAPIView.as_view(), name="login" ),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('client_profiles/', views.client_profile_list, name='client_profiles'),
    path('pharma_profiles/', views.pharmacist_profile_list, name='pharma_profiles'),
    path('verify/', ClientVerifyView.as_view(), name="verify" ),
    path('update_client_profile/', ClientUpdateProfileView.as_view(), name="update_client_profile" ),
    path('update_pharma_profile/', PharmaUpdateProfileView.as_view(), name="update_pharma_profile" ),
    path('go_live/', GoLiveView.as_view(), name="go_live"),
    path('client_details/<str:uuid>/', ClientDetailView.as_view(), name="client_details" ),
    path('care_form/', CareFormView.as_view(), name='care_form'),
    path('referral/', PharmacistReferral.as_view(), name='referral'),
    path('admin_care_form/', AdminCareFormView.as_view(), name='admin_care_form'),
    path('care_form/<str:uuid>/', AdminDetailCareformView.as_view(), name='care_form_detail'),
    path('pharma_details/<str:uuid>/', PharmacistDetailView.as_view(), name="pharma_details" ),
    path('referred_clients/', ReferredClientsListAPIView.as_view(), name='referred_clients'),
    path('change_password/', ChangePasswordView.as_view(), name='change-password'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')), 
    # To confirm the paswsword, the endpoint will be /password_reset/confirm/
    path('password_reset/confirm/', include('django_rest_passwordreset.urls', namespace='password_reset_confirm')),
    # Mnitor User Activity and History
    path('activity/', UserActivityView.as_view(), name='activity'),
    path('user_activity/', AdminUserActivityView.as_view(), name='user_activity'),
    # Payment
    path('make_payment/', views.make_payment, name='make_payment'),
    path('verify_payment/<str:reference>/', VerifyPayment.as_view(), name='verify_payment'),
    # Dashboard
    path('client_dashboard/', ClientDashboardView.as_view(), name='client_dashboard'),
    path('pharmacist_dashboard/', PharmacistDashboardView.as_view(), name='pharmacist_dashboard'),
    
]
