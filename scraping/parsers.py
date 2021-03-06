import requests
import codecs
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent

headers = {'User-Agent': UserAgent().random}


def parse_superjob(url, city=None, language=None):
    vacancy_list = []
    errors_list = []

    domain = 'https://habarovsk.superjob.ru'
    # url = 'https://habarovsk.superjob.ru/vacancy/search/?keywords=python'

    if url:
        resp = requests.get(url, headers=headers)

        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            div_lst = soup.find_all('div', attrs={'class': 'f-test-vacancy-item'})

            if div_lst:
                for div in div_lst:
                    link = div.select('a[class*="f-test-link"]')
                    title = link[0]
                    href = link[0]['href']
                    company = link[-1]
                    company_name = company.text if company else 'Нет данных'
                    link_parent = link[-1].find_parent('div').find_parent('div').find_parent('div').find_parent(
                        'div').find_parent('div')
                    div_sibling = link_parent.find_next_sibling('div')
                    span = div_sibling.select('span')
                    short_desc = span[0].text
                    vacancy_list.append(
                        {'title': title.text, 'url': domain + href, 'description': short_desc, 'company': company_name,
                         'city_id': city, 'language_id': language})
            else:
                errors_list.append({'url': url, 'title': 'Искомый элемент разметки не существует'})
        else:
            errors_list.append({'url': url, 'title': 'Сайт не отвечает'})
    return vacancy_list, errors_list


def parse_headhunter(url, city=None, language=None):
    vacancy_list = []
    errors_list = []

    # url = 'https://khabarovsk.hh.ru/search/vacancy?text=python&from=suggest_post&fromSearchLine=true&area=102'

    if url:
        resp = requests.get(url, headers=headers)

        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            div_lst = soup.find_all('div', attrs={'class': 'serp-item'})

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
                        {'title': title.text, 'url': href, 'description': short_desc, 'company': company_name,
                         'city_id': city, 'language_id': language})
            else:
                errors_list.append({'url': url, 'title': 'Искомый элемент разметки не существует'})
        else:
            errors_list.append({'url': url, 'title': 'Сайт не отвечает'})
    return vacancy_list, errors_list


def parse_rabota(url, city=None, language=None):
    vacancy_list = []
    errors_list = []

    domain = 'https://khabarovsk.rabota.ru'
    # url = 'https://khabarovsk.rabota.ru/?query=python&sort=relevance'

    if url:
        resp = requests.get(url, headers=headers)

        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            div = soup.find('div', attrs={'class': 'home-vacancies__infinity-list'})
            elem_lst = div.select('.r-home-serp__item')
            if elem_lst:
                for item in elem_lst:
                    if 'r-serp-similar-title' in item['class']:
                        break
                    if 'vacancy-preview-card' in item['class']:
                        title = item.find('h3', attrs={'class': 'vacancy-preview-card__title'})
                        href = title.a['href']
                        short_desc = item.find('div', attrs={'class': 'vacancy-preview-card__short-description'})
                        company_name = item.find('span', attrs={'class': 'vacancy-preview-card__company-name'})
                        vacancy_list.append(
                            {'title': title.text.strip(), 'url': domain + href, 'description': short_desc.text,
                             'company': company_name.text, 'city_id': city, 'language_id': language})
            else:
                errors_list.append({'url': url, 'title': 'Искомый элемент разметки не существует'})
        else:
            errors_list.append({'url': url, 'title': 'Сайт не отвечает'})
    return vacancy_list, errors_list


if __name__ == '__main__':
    url = 'https://habarovsk.superjob.ru/vacancy/search/?keywords=python'
    # url = 'https://khabarovsk.hh.ru/search/vacancy?text=python&from=suggest_post&fromSearchLine=true&area=102'
    # url = 'https://khabarovsk.rabota.ru/?query=python&sort=relevance'
    data, errors = parse_superjob(url)
    # data, errors = parse_headhunter(url)
    # data, errors = parse_rabota(url)
    with codecs.open('test.txt', 'w', encoding='utf-8') as file_handler:
        file_handler.write(str(data))
