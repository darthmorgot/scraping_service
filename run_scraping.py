import codecs
import os
import sys

from django.db import DatabaseError

project_path = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'

import django
django.setup()

from scraping.parsers import parse_superjob, parse_headhunter, parse_rabota
from scraping.models import Vacancy, City, Language, Error

parsers = (
    (parse_superjob, 'https://habarovsk.superjob.ru/vacancy/search/?keywords=python'),
    (parse_headhunter,
     'https://khabarovsk.hh.ru/search/vacancy?text=python&from=suggest_post&fromSearchLine=true&area=102'),
    (parse_rabota, 'https://khabarovsk.rabota.ru/?query=python&sort=relevance')
)

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
