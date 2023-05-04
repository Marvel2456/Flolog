from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)
from .views import ClientRegisterView, LoginAPIView, PharmacistRegisterView, ClientVerifyView
from . import views



urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register_client/', ClientRegisterView.as_view(), name="register_client" ),
    path('register_pharma/', PharmacistRegisterView.as_view(), name="register_pharma" ),
    path('login/', LoginAPIView.as_view(), name="login" ),
    path('client_profiles/', views.client_profile_list, name='client_profiles'),
    path('verify/', ClientVerifyView.as_view(), name="verify" ),
]
