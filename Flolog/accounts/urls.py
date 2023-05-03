from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)
from .views import ClientRegisterView, LoginAPIView



urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register_client/', ClientRegisterView.as_view(), name="register_client" ),
    path('login/', LoginAPIView.as_view(), name="login" ),
]
