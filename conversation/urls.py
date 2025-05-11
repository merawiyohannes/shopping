from django.urls import path
from . import views

urlpatterns = [
    path("chat-super/<int:pk>", views.message_view, name="message_view"),
    path("chat-super", views.chat_view, name="chat_view"),
    path("chat-user", views.contact_view, name='contact_view'),
    path("chat-user/<int:pk>", views.super_view, name='super_view')
]
