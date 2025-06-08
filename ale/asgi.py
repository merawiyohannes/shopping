"""
ASGI config for ale project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ale.settings')
django_asgi_app = get_asgi_application()
from channels.routing import ProtocolTypeRouter, URLRouter
from conversation.routing import websocket_urlpatterns
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
})  

