from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home_view"),
    path("detail/<int:pk>", views.detail_view, name='detail_view')
]
