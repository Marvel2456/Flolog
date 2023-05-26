from django.urls import path
from .views import HomeView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('<str:ref_code>/', HomeView.as_view(), name='home'),
]
