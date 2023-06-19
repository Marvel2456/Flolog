from django.urls import path
from . import views

urlpatterns = [
    path('social-auth/', views.social_auth, name='social-auth'),
]
