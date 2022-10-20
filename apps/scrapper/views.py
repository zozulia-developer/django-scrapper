from django.views.generic import FormView
from django.views.generic.list import ListView

from apps.scrapper import models, forms


class HomeView(FormView):
    form_class = forms.FindForm
    template_name = "scrapper/home.html"


class VacanciesList(ListView):
    model = models.Vacancy
    form = forms.FindForm
    paginate_by = 10
    template_name = "scrapper/list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["city"] = self.request.GET.get("city")
        context["language"] = self.request.GET.get("language")
        context["form"] = self.form
        return context

    def get_queryset(self):
        city = self.request.GET.get("city")
        language = self.request.GET.get("language")
        qs = []
        if city or language:
            _filter = {}
            if city:
                _filter["city__slug"] = city
            if language:
                _filter["language__slug"] = language
            qs = models.Vacancy.objects.filter(**_filter).select_related("city", "language")
        return qs
