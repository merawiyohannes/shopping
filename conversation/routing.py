from django.urls import re_path, path
from .consumers import ChatConsumers, NotifyConsumer


websocket_urlpatterns = [
    path('ws/chat-super/<int:room_number>/', ChatConsumers.as_asgi()),
    path('ws/chat-user/<int:room_number>/', ChatConsumers.as_asgi()),
    path('ws/notify/', NotifyConsumer.as_asgi()),
]