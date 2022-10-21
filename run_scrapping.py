import asyncio
import datetime
import os
import sys
from django.db import DatabaseError
from django.contrib.auth import get_user_model

proj = os.path.dirname(os.path.abspath("manage.py"))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "core.settings"

import django
django.setup()

from apps.scrapper.parsers import *
from apps.scrapper import models


User = get_user_model()


parsers = (
    (work, "work"),
    # (rabota, "rabota"),
    (dou, "dou"),
    (djinni, "djinni"),
)
jobs, errors = [], []


def get_settings():
    qs = User.objects.filter(send_email=True, is_active=True).values()
    settings_list = set((q['city_id'], q['language_id']) for q in qs)
    return settings_list


def get_urls(_settings):
    qs = models.Url.objects.all().values()
    url_dict = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        if pair in url_dict:
            tmp = {}
            tmp['city'] = pair[0]
            tmp['language'] = pair[1]
            tmp['url_data'] = url_dict[pair]
            urls.append(tmp)
    return urls


async def main(value):
    func, url, city, language = value
    job, err = await loop.run_in_executor(None, func, url, city, language)
    errors.extend(err)
    jobs.extend(job)

settings = get_settings()
url_list = get_urls(settings)


loop = asyncio.get_event_loop()
tmp_tasks = [(func, data['url_data'][key], data['city'], data['language'])
             for data in url_list
             for func, key in parsers]
tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])
loop.run_until_complete(tasks)
loop.close()


for job in jobs:
    v = models.Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
    qs = models.Error.objects.filter(timestamp=datetime.date.today())
    if qs.exists():
        err = qs.first()
        data = err.data
        err.data.update({'errors': errors})
        err.save()
    else:
        er = models.Error(data=f'errors:{errors}')
        er.save()

ten_days_ago = datetime.date.today() - datetime.timedelta(days=10)
models.Vacancy.objects.filter(timestamp__lte=ten_days_ago).delete()
