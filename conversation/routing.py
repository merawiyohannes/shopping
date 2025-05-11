from django.urls import re_path, path
from .consumers import ChatConsumers, notification


websocket_urlpatterns = [
    path('ws/chat-super/<int:room_number>/', ChatConsumers.as_asgi()),
    path('ws/chat-user/<int:room_number>/', ChatConsumers.as_asgi()),
    path('ws/', ChatConsumers.as_asgi()),
    
]