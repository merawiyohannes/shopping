from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from .forms import LoginForm
from . import views

urlpatterns = [
    path("signup/", views.signup_view, name='signup_view'),
    path('login/', LoginView.as_view(template_name="authentication/login.html", authentication_form=LoginForm), name='login_view'),
    path('logout/', LogoutView.as_view(), name="logout_view"),
    path('change-password/', views.psw_change_view, name='change_password')
]
