import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView, DeleteView, UpdateView

from apps.accounts import forms
from apps.scrapper import models

User = get_user_model()


class LoginUserView(FormView):
    form_class = forms.UserLoginForm
    success_url = reverse_lazy("home")
    template_name = "accounts/login.html"

    def form_valid(self, form):
        user = authenticate(
            self.request,
            username=form.cleaned_data["email"],
            password=form.cleaned_data["password"]
        )
        if user and user.is_active:
            login(self.request, user)
            return redirect("home")
        return redirect("login")


def logout_view(request):
    logout(request)
    return redirect("home")


class RegisterUserView(CreateView):
    form_class = forms.UserRegistrationForm
    template_name = "accounts/register.html"

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data["password"])
        new_user.save()
        messages.success(self.request, "New user created!")
        return render(self.request, "accounts/register_done.html", {"new_user": new_user})


class UpdateUserView(LoginRequiredMixin, UpdateView):
    form_class = forms.UserUpdateForm
    contact_form = forms.ContactForm
    template_name = "accounts/update.html"

    def post(self, request, *args, **kwargs):
        form = forms.UserUpdateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = request.user
            user.city = data["city"]
            user.language = data["language"]
            user.send_email = data["send_email"]
            user.save()
            messages.success(request, "User updated successfully!")
            return redirect("accounts:update")

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial={
            "city": request.user.city,
            "language": request.user.language,
            "send_email": request.user.send_email
        })
        return render(request, "accounts/update.html", {"form": form, "contact_form": self.contact_form})


class DeleteUserView(LoginRequiredMixin, DeleteView):

    def post(self, request, *args, **kwargs):
        user = request.user
        qs = User.objects.get(pk=user.pk)
        qs.delete()
        messages.success(request, "User deleted successfully!")
        return redirect("home")


class ContactFromView(LoginRequiredMixin, FormView):
    form_class = forms.ContactForm
    success_url = reverse_lazy("update")

    def form_valid(self, form):
        data = form.cleaned_data
        city = data.get("city")
        language = data.get("language")
        email = data.get("email")
        qs = models.Error.objects.filter(timestamp=datetime.date.today())
        if qs.exists():
            err = qs.first()
            data = err.data.get("user_data", [])
            data.append({'city': city, 'language': language, 'email': email})
            err.data["user_data"] = data
            err.save()
        else:
            data = [{'city': city, 'language': language, 'email': email}]
            models.Error(data=f"user_data:{data}").save()
            messages.success(self.request, "Data sent to administrator!")
            return redirect("accounts:update")
