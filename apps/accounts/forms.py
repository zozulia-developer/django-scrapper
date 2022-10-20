from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

from apps.scrapper import models

User = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email").strip()
        password = self.cleaned_data.get("password")

        if email and password:
            qs = User.objects.filter(email=email)
            if not qs.exists():
                raise forms.ValidationError('There is no such user!')
            if not check_password(password, qs[0].password):
                raise forms.ValidationError('Password is incorrect!')
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('This account is not active!')
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    email = forms.CharField(
        label="Enter email",
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        label="Enter password",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label="Repeat password",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ['email']

    def clean_password2(self):
        data = self.cleaned_data
        if data["password"] != data["password2"]:
            raise forms.ValidationError("Passwords don't match!")
        return data["password2"]


class UserUpdateForm(forms.Form):
    city = forms.ModelChoiceField(
        queryset=models.City.objects.all(),
        to_field_name="slug",
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="City"
    )
    language = forms.ModelChoiceField(
        queryset=models.Language.objects.all(),
        to_field_name="slug",
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Language"
    )
    send_email = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput,
        label="Get newsletter ?"
    )

    class Meta:
        model = User
        fields = ['city', 'language', 'send_email']


class ContactForm(forms.Form):
    city = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="City"
    )
    language = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Language"
    )
    email = forms.CharField(
        required=True,
        label="Enter email",
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )
