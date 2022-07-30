import os
import sys
import django
import datetime

from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model

project_path = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'

django.setup()
from scraping_service.settings import EMAIL_HOST_USER
from scraping.models import Vacancy, Error, Url
User = get_user_model()

ADMIN_EMAIL = EMAIL_HOST_USER
today = datetime.date.today()
subject = f'Рассылка вакансий от Scraping за {today}'
text_content = f'Рассылка вакансий от Scraping за {today}.'
from_email = EMAIL_HOST_USER
to_email = 'to@example.com'
empty = '<h2>По вашему запросу ничего не найдено.</h2>'

user_data = User.objects.filter(send_email=True).values('city', 'language', 'city__name', 'language__name', 'email')
users_dict = {}
for item in user_data:
    users_dict.setdefault((item['city'], item['language'], item['city__name'], item['language__name']), [])
    users_dict[(item['city'], item['language'], item['city__name'], item['language__name'])].append(item['email'])

if users_dict:
    params = {'city_id__in': [], 'language_id__in': []}
    for pair in users_dict.keys():
        params['city_id__in'].append(pair[0])
        params['language_id__in'].append(pair[1])
    vacancy_data = Vacancy.objects.filter(**params, timestamp=today).values()
    vacancies = {}
    for item in vacancy_data:
        vacancies.setdefault((item['city_id'], item['language_id']), [])
        vacancies[(item['city_id'], item['language_id'])].append(item)
    for keys, emails in users_dict.items():
        rows = vacancies.get(keys, [])
        html = ''
        for row in rows:
            html += f'<h4><a href="{row["url"]}">{row["title"]}</a></h4>'
            html += f'<p>{row["description"]}</p>'
            html += f'<p>{row["company"]}</p><br><hr>'
        html_content = html if html else empty
        for email in emails:
            to_email = email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

error_data = Error.objects.filter(timestamp=today)
subject = ''
text_content = ''
to_email = ADMIN_EMAIL
html_content = ''

if error_data.exists():
    error = error_data.first()
    data = error.data
    for item in data:
        html_content += f'<h4><a href="{item["url"]}">Error: {item["title"]}</a></h4>'

    subject += f'Ошибки выполнения скрапинга {today} '
    text_content += 'Ошибки выполнения скрапинга'

url_data = Url.objects.all().values('city', 'language')
urls_dict = {(i['city'], i['language']): True for i in url_data}
url_error = ''
for keys in users_dict:
    if keys not in urls_dict:
        url_error += f'<p>Для города: {keys[2]} и ЯП: {keys[3]} нет подходящих ссылок.</p>'

if url_error:
    subject += 'Отсутствующие ссылки '
    html_content += url_error

if subject:
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
