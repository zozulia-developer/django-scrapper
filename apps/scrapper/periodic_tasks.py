import datetime

from apps.scrapper import models
from apps.scrapper.services import parser_service
from core.celery import app


@app.task(bind=True)
def delete_old_vacancies(self):
    ten_days_ago = datetime.date.today() - datetime.timedelta(days=10)
    vacancies = models.Vacancy.objects.filter(timestamp__lte=ten_days_ago)
    vacancies_count = vacancies.count()
    vacancies.delete()
    return f"Deleted {vacancies_count} vacancies!"


@app.task(bind=True)
def run_scrapping(self):
    parse_service = parser_service.ParserService()
    parse_service.run()
