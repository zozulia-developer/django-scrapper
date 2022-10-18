from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model

from apps.accounts import forms


User = get_user_model()


def login_view(request):
    form = forms.UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        email = data.get("email")
        password = data.get("password")
        user = authenticate(request, username=email, password=password)
        login(request, user)
        return redirect("home")
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")


def register_view(request):
    form = forms.UserRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data["password"])
        new_user.save()
        messages.success(request, "New user has added!")
        return render(request, "accounts/register_done.html", {"new_user": new_user})
    return render(request, "accounts/register.html", {"form": form})


def update_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == "POST":
            form = forms.UserUpdateForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user.city = data["city"]
                user.language = data["language"]
                user.send_email = data["send_email"]
                user.save()
                messages.success(request, "User updated successful!")
                return redirect("accounts:update")
        form = forms.UserUpdateForm(initial={
            "city": user.city,
            "language": user.language,
            "send_email": user.send_email
        })
        return render(request, "accounts/update.html", {"form": form})
    else:
        return redirect("accounts:login")


def delete_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == "POST":
            qs = User.objects.get(pk=user.pk)
            qs.delete()
            messages.error(request, "User has been deleted!")
    return redirect("home")
