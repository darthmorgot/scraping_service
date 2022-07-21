import codecs
import os
import sys

from django.contrib.auth import get_user_model
from django.db import DatabaseError

project_path = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'

import django

django.setup()

from scraping.parsers import parse_superjob, parse_headhunter, parse_rabota
from scraping.models import Vacancy, City, Language, Error, Url

User = get_user_model()

parsers = (
    (parse_superjob, 'https://habarovsk.superjob.ru/vacancy/search/?keywords=python'),
    (parse_headhunter,
     'https://khabarovsk.hh.ru/search/vacancy?text=python&from=suggest_post&fromSearchLine=true&area=102'),
    (parse_rabota, 'https://khabarovsk.rabota.ru/?query=python&sort=relevance')
)


def get_user_data():
    user_data = User.objects.filter(send_email=True).values()
    data_list = set((i['city_id'], i['language_id']) for i in user_data)
    return data_list


def get_urls(settings):
    url_data = Url.objects.all().values()
    url_dict = {(i['city_id'], i['language_id']): i['url_data'] for i in url_data}
    urls = []
    for pair in settings:
        tmp = {'city': pair[0], 'language': pair[1], 'url_data': url_dict[pair]}
        urls.append(tmp)
    return urls


city = City.objects.filter(slug='habarovsk').first()
language = Language.objects.filter(slug='python').first()

data = []
errors = []

for func, url in parsers:
    data_result, errors_result = func(url)
    data += data_result
    errors += errors_result

for item in data:
    vacancy = Vacancy(**item, city=city, language=language)
    try:
        vacancy.save()
    except DatabaseError:
        pass

if errors:
    ers = Error(data=errors).save()

# with codecs.open('parsing_result.txt', 'w', encoding='utf-8') as file_handler:
#     file_handler.write(str(data))
