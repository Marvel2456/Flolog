from django.urls import path, include
from .views import *
from . import routing


urlpatterns = [
    path('request_chat/', RequestChatView.as_view(), name='request_chat'),
    path('view_chat_request/', ViewChatRequests.as_view(), name='view_chat_request'),
    path('/ws/<chatroom_id>/', include(routing.websocket_urlpatterns)),
    
]
