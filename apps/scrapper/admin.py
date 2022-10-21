from django.contrib import admin

from apps.scrapper import models


class CityAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]


class LanguageAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]


class VacancyAdmin(admin.ModelAdmin):
    list_display = ["title", "company", "city", "language", "timestamp"]
    list_select_related = ["city", "language"]
    search_fields = ["title"]


class UrlAdmin(admin.ModelAdmin):
    list_display = ["city", "language", "url_data"]
    list_select_related = ["city", "language"]


class ErrorAdmin(admin.ModelAdmin):
    list_display = ["data", "timestamp"]


admin.site.register(models.City, CityAdmin)
admin.site.register(models.Language, LanguageAdmin)
admin.site.register(models.Vacancy, VacancyAdmin)
admin.site.register(models.Error, ErrorAdmin)
admin.site.register(models.Url, UrlAdmin)
