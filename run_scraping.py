import asyncio
import codecs
import os
import sys
import datetime

from django.contrib.auth import get_user_model
from django.db import DatabaseError

project_path = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'

import django

django.setup()

from scraping.parsers import parse_superjob, parse_headhunter, parse_rabota
from scraping.models import Vacancy, Error, Url

User = get_user_model()

parsers = (
    (parse_superjob, 'superjob'),
    (parse_headhunter, 'headhunter'),
    (parse_rabota, 'rabota')
)
data = []
errors = []


def get_user_data():
    user_data = User.objects.filter(send_email=True).values()
    data_list = set((i['city_id'], i['language_id']) for i in user_data)
    return data_list


def get_urls(settings):
    url_data = Url.objects.all().values()
    url_dict = {(i['city_id'], i['language_id']): i['url_data'] for i in url_data}
    urls = []
    for pair in settings:
        if pair in url_dict:
            tmp = {'city': pair[0], 'language': pair[1], 'url_data': url_dict[pair]}
            urls.append(tmp)
    return urls


async def main(value):
    func, url, city, language = value
    data_item, error = await loop.run_in_executor(None, func, url, city, language)
    errors.extend(error)
    data.extend(data_item)


user_settings = get_user_data()
url_list = get_urls(user_settings)

loop = asyncio.get_event_loop()
tmp_tasks = [
    (func, data_item['url_data'][url_key], data_item['city'], data_item['language'])
    for data_item in url_list
    for func, url_key in parsers
]
tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])

# for data_item in url_list:
#     for func, url_key in parsers:
#         url = data_item['url_data'][url_key]
#         data_result, errors_result = func(url, city=data_item['city'], language=data_item['language'])
#         data += data_result
#         errors += errors_result

loop.run_until_complete(tasks)
loop.close()

for item in data:
    vacancy = Vacancy(**item)
    try:
        vacancy.save()
    except DatabaseError:
        pass

if errors:
    error_data = Error.objects.filter(timestamp=datetime.date.today())
    if error_data.exists():
        err = error_data.first()
        err.data.update({'errors': errors})
        err.save()
    else:
        ers = Error(data=f'errors: {errors}').save()

# with codecs.open('parsing_result.txt', 'w', encoding='utf-8') as file_handler:
#     file_handler.write(str(data))

data_retention_period = datetime.date.today() - datetime.timedelta(7)
Vacancy.objects.filter(timestamp__lte=data_retention_period).delete()
