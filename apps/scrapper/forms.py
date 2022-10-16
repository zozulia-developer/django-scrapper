from django import forms

from apps.scrapper import models


class FindForm(forms.Form):
    city = forms.ModelChoiceField(
        queryset=models.City.objects.all(),
        to_field_name="slug",
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="City"
    )
    language = forms.ModelChoiceField(
        queryset=models.Language.objects.all(),
        to_field_name="slug",
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Language"
    )
