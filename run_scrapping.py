import os
import sys
from django.db import DatabaseError

proj = os.path.dirname(os.path.abspath("manage.py"))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "core.settings"

import django
django.setup()

from apps.scrapper.parsers import *
from apps.scrapper import models


parsers = (
    (work, "https://www.work.ua/ru/jobs-kyiv-python/"),
    # (rabota, "https://rabota.ua/ua/zapros/python/%D1%83%D0%BA%D1%80%D0%B0%D0%B8%D0%BD%D0%B0djinni"),
    (dou, "https://jobs.dou.ua/vacancies/?search=python"),
    (djinni, "https://djinni.co/jobs/?region=UKR&primary_keyword=Python"),
)

city = models.City.objects.filter(slug="kiev").first()
language = models.Language.objects.filter(slug="python").first()

jobs, errors = [], []
for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e

for job in jobs:
    v = models.Vacancy(**job, city=city, language=language)
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
    er = models.Error(data=errors)
    er.save()
