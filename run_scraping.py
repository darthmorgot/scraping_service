import codecs

from scraping.parsers import parse_superjob, parse_headhunter, parse_rabota

parsers = (
    (parse_superjob, 'https://habarovsk.superjob.ru/vacancy/search/?keywords=python'),
    (parse_headhunter,
     'https://khabarovsk.hh.ru/search/vacancy?text=python&from=suggest_post&fromSearchLine=true&area=102'),
    (parse_rabota, 'https://khabarovsk.rabota.ru/?query=python&sort=relevance')
)

data = []
errors = []

for func, url in parsers:
    data_result, errors_result = func(url)
    data += data_result
    errors += errors_result

with codecs.open('parsing_result.txt', 'w', encoding='utf-8') as file_handler:
    file_handler.write(str(data))
