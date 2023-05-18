from django.urls import path, include
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)
from .views import (ClientRegisterView, PharmacistRegisterView, 
                    ClientVerifyView,ClientDetailView, PharmacistDetailView,
                    PharmaUpdateProfileView, ClientUpdateProfileView, ChangePasswordView,
                    LoginAPIView, GoLiveView, )
from . import views



urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register_client/', ClientRegisterView.as_view(), name="register_client" ),
    path('register_pharma/', PharmacistRegisterView.as_view(), name="register_pharma" ),
    path('login/', LoginAPIView.as_view(), name="login" ),
    path('client_profiles/', views.client_profile_list, name='client_profiles'),
    path('pharma_profiles/', views.pharmacist_profile_list, name='pharma_profiles'),
    path('verify/', ClientVerifyView.as_view(), name="verify" ),
    path('update_client_profile/', ClientUpdateProfileView.as_view(), name="update_client_profile" ),
    path('update_pharma_profile/', PharmaUpdateProfileView.as_view(), name="update_pharma_profile" ),
    path('go_live/', GoLiveView.as_view(), name="go_live"),
    path('client_details/<str:uuid>/', ClientDetailView.as_view(), name="client_details" ),
    path('pharma_details/<str:uuid>/', PharmacistDetailView.as_view(), name="pharma_details" ),
    path('change_password/', ChangePasswordView.as_view(), name='change-password'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')), 
    # To confirm the paswsword, the endpoint will be /password_reset/confirm/
    path('password_reset/confirm/', include('django_rest_passwordreset.urls', namespace='password_reset_confirm')),
]
