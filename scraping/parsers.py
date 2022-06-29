import requests
import codecs
from bs4 import BeautifulSoup as BS

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}


def parse_superjob(url):
    vacancy_list = []
    errors_list = []

    domain = 'https://habarovsk.superjob.ru'
    # url = 'https://habarovsk.superjob.ru/vacancy/search/?keywords=python'

    resp = requests.get(url, headers=headers)

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
                company = div.find('span', attrs={'class': 'f-test-text-vacancy-item-company-name'})
                company_name = company.text if company else 'Нет данных'
                vacancy_list.append(
                    {'title': title.text, 'url': domain + href, 'description': short_desc, 'company': company_name})
        else:
            errors_list.append({'url': url, 'title': 'Искомый элемент разметки не существует'})
    else:
        errors_list.append({'url': url, 'title': 'Сайт не отвечает'})
    return vacancy_list, errors_list


def parse_headhunter(url):
    vacancy_list = []
    errors_list = []

    domain = 'https://khabarovsk.hh.ru'

    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        div_lst = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})

        if div_lst:
            for div in div_lst:
                heading = div.find('h3', attrs={'class': 'bloko-header-section-3'})
                title = heading.find('a', attrs={'class': 'bloko-link'})
                href = title['href']
                company = div.find('div', attrs={'class': 'vacancy-serp-item__meta-info-company'})
                company_name = company.a.text if company else 'Нет данных'
                div_elem = div.find('div', attrs={'class': 'g-user-content'})
                div_block_lst = div_elem.find_all('div', attrs={'class': 'bloko-text'})
                short_desc = ''
                for elem in div_block_lst:
                    short_desc += elem.text
                vacancy_list.append(
                    {'title': title.text, 'url': href, 'description': short_desc, 'company': company_name})
        else:
            errors_list.append({'url': url, 'title': 'Искомый элемент разметки не существует'})
    else:
        errors_list.append({'url': url, 'title': 'Сайт не отвечает'})
    return vacancy_list, errors_list


if __name__ == '__main__':
    url = 'https://khabarovsk.hh.ru/search/vacancy?' \
          'area=102&search_field=name&search_field=company_name&search_field=description&text=python' \
          '&from=suggest_post&clusters=true&ored_clusters=true&enable_snippets=true'
    data, errors = parse_headhunter(url)
    with codecs.open('test.txt', 'w', encoding='utf-8') as file_handler:
        file_handler.write(str(data))
