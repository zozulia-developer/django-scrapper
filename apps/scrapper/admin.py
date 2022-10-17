from django.contrib import admin

from apps.scrapper import models


admin.site.register(models.City)
admin.site.register(models.Language)
admin.site.register(models.Vacancy)
admin.site.register(models.Error)
admin.site.register(models.Url)
