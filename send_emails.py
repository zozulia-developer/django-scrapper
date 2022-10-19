import os
import sys
import django
import datetime
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives

proj = os.path.dirname(os.path.abspath("manage.py"))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "core.settings"

django.setup()
from apps.scrapper import models
from core import settings

today = datetime.date.today()
subject = f"Newsletter vacancies for {today}"
text_content = f"Newsletter vacancies {today}"
from_email = settings.EMAIL_HOST_USER
empty = '<h2>Nothing found!</h2>'
User = get_user_model()

qs = User.objects.filter(send_email=True).values('city', 'language', 'email')
users_dict = {}
for i in qs:
    users_dict.setdefault((i['city'], i['language']), [])
    users_dict[(i['city'], i['language'])].append(i['email'])

if users_dict:
    params = {'city_id__in': [], 'language_id__in': []}
    for pair in users_dict.keys():
        params['city_id__in'].append(pair[0])
        params['language_id__in'].append(pair[1])
    qs = models.Vacancy.objects.filter(**params, timestamp=today).values()[:10]
    vacancies = {}
    for i in qs:
        vacancies.setdefault((i['city_id'], i['language_id']), [])
        vacancies[(i['city_id'], i['language_id'])].append(i)
    for keys, emails in users_dict.items():
        rows = vacancies.get(keys, [])
        html = ""
        for row in rows:
            html += f'<h5><a href="{row["url"]}">{row["title"]}</a></h5>'
            html += f'<p>{row["description"]}</p>'
            html += f'<p>{row["company"]}</p><br><hr>'
        _html = html if html else empty
        for email in emails:
            to = email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(_html, "text/html")
            msg.send()

ADMIN_USER = User.objects.filter(send_email=True, is_admin=True).first()
qs = models.Error.objects.filter(timestamp=today)
subject = ""
text_content = ""
_html = ""
to = ADMIN_USER.email

if qs.exists():
    error = qs.first()
    data = error.data.get("errors", [])

    for i in data:
        _html += f'<p><a href="{i["url"]}">Error: {i["title"]}</a></h3><p><br>'
        subject = f"Scrapping errors - {today}!"
        text_content = f"Scrapping errors!"
        data = error.data.get("user_data")
        if data:
            _html += "<hr>"
            _html += "<h2>Subs commit!</h2>"
            for i in data:
                _html += f'<p>City: {i["city"]}, Language: {i["language"]}, Email: {i["email"]}<p><br>'
                subject = f"Subs commit!"
                text_content = f"Subs commit!"

qs = models.Url.objects.all().values('city', 'language')
urls_dict = {(i['city'], i['language']): True for i in qs}
urls_errors = ""

for keys in users_dict.keys():
    if keys not in urls_dict:
        if keys[0] and keys[1]:
            urls_errors += f'<p>City: {keys[0]}, Language: {keys[1]}, urls not found!</p><br>'

if urls_errors:
    subject += " Urls not found!"
    _html += urls_errors

if subject:
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(_html, "text/html")
    msg.send()
