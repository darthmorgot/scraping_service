import requests
import codecs
from bs4 import BeautifulSoup as BS


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

domain = 'https://habarovsk.superjob.ru'
url = 'https://habarovsk.superjob.ru/vacancy/search/?keywords=python'

resp = requests.get(url, headers=headers)
data = []
errors = []

if resp.status_code == 200:
    soup = BS(resp.content, 'html.parser')
    div_lst = soup.find_all('div', attrs={'class': 'f-test-vacancy-item'})

    if div_lst:
        for div in div_lst:
            title = div.find('span', attrs={'class': '_37mRb'})
            href = title.a['href']
            div_elem = div.find('div', attrs={'class': '_2SZOi'})
            span = div_elem.find('span', attrs={'class': '_1AFgi'})
            short_desc = span.text
            name = div.find('span', attrs={'class': 'f-test-text-vacancy-item-company-name'})
            company = name.text if name else 'Нет данных'
            data.append({'title': title.text, 'url': domain + href, 'description': short_desc, 'company': company})
    else:
        errors.append({'url': url, 'title': 'Искомый div не существует'})
else:
    errors.append({'url': url, 'title': 'Сайт не отвечает'})

with codecs.open('test.txt', 'w', encoding='utf-8') as file_handler:
    file_handler.write(str(data))
