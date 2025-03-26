from django.urls import path
from . import views

urlpatterns = [
    path("chat/<int:pk>", views.message_view, name="message_view"),
    path("people/", views.chat_view, name="chat_view"),
    path("message/", views.contact_view, name='contact_view'),
    path("super/<int:pk>", views.super_view, name='super_view')
]
