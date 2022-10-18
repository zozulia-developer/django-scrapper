from django.shortcuts import render
from django.core.paginator import Paginator
from apps.scrapper import models, forms


def home_view(request):
    form = forms.FindForm()

    return render(request, "scrapper/home.html", {"form": form})


def list_view(request):
    form = forms.FindForm()
    city = request.GET.get("city")
    language = request.GET.get("language")
    context = {'city': city, 'language': language, 'form': form}

    if city or language:
        _filter = {}
        if city:
            _filter["city__slug"] = city
        if language:
            _filter["language__slug"] = language
        qs = models.Vacancy.objects.filter(**_filter)
        paginator = Paginator(qs, 10)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['object_list'] = page_obj

    return render(request, "scrapper/list.html", context)
