import datetime

from django.contrib.auth import get_user_model
from django.db import DatabaseError

from apps.scrapper import models
from apps.scrapper.services import parsers


class ParserService:
    jobs, errors = [], []
    User = get_user_model()
    parsers = (
        (parsers.WorkUaParser().parse, "work"),
        (parsers.DouParser().parse, "dou"),
        (parsers.DjinniParser().parse, "djinni"),
    )

    @classmethod
    def _get_settings(cls):
        qs = cls.User.objects.filter(send_email=True, is_active=True).values()
        settings_list = set((q['city_id'], q['language_id']) for q in qs)
        return settings_list

    @classmethod
    def _get_urls(cls, _settings):
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

    def _save_jobs(self):
        for job in self.jobs:
            v = models.Vacancy(**job)
            try:
                v.save()
            except DatabaseError:
                pass

    def _save_errors(self):
        if self.errors:
            qs = models.Error.objects.filter(timestamp=datetime.date.today())
            if qs.exists():
                err = qs.first()
                err.data.update({'errors': self.errors})
                err.save()
            else:
                er = models.Error(data=f'errors:{self.errors}')
                er.save()

    def run(self):
        settings = self._get_settings()
        url_list = self._get_urls(settings)

        for func, key in self.parsers:
            for data in url_list:
                job, err = func(url=data['url_data'][key], city=data['city'], language=data['language'])
                self.errors.extend(err)
                self.jobs.extend(job)

        self._save_jobs()
        self._save_errors()
