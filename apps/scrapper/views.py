from django.shortcuts import render
from apps.scrapper import models, forms


def home_view(request):
    form = forms.FindForm()
    city = request.GET.get("city")
    language = request.GET.get("language")
    qs = []

    if city or language:
        _filter = {}
        if city:
            _filter["city__slug"] = city
        if language:
            _filter["language__slug"] = language
        qs = models.Vacancy.objects.filter(**_filter)

    return render(request, "scrapper/home.html", {"object_list": qs, "form": form})
