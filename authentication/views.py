from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash

from .forms import SignupForm, PswChangeForm

def psw_change_view(request):
    form = PswChangeForm(user=request.user)
    if request.method == 'POST':
        form = PswChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('dashboard_view')
    else:
        form = PswChangeForm(user=request.user)
    return render(request, 'authentication/change_password.html', {"form":form})

def signup_view(request):
    form = SignupForm()
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login_view")
    else:
        form = SignupForm()
        
    return render(request, "authentication/signup.html", {"form":form})
