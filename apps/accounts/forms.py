from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

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
