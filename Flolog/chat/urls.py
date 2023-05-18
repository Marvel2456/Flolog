from django.urls import path
from .views import *


urlpatterns = [
    path('request_chat/', RequestChatView.as_view(), name='request_chat'),
    path('view_chat_request/', ViewChatRequests.as_view(), name='view_chat_request'),
    
]
