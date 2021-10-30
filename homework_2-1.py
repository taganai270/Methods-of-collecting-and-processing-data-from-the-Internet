from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

"""
    Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы)
    с сайтов Superjob и HH. Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
    Получившийся список должен содержать в себе минимум:
     Наименование вакансии.
     Предлагаемую зарплату (отдельно минимальную и максимальную).
     Ссылку на саму вакансию.
     Сайт, откуда собрана вакансия.
    По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение). 
    Структура должна быть одинаковая для вакансий с обоих сайтов. 

"""

CSV = 'vacancy.csv' # файл с полученными данными
HOST = 'https://ekaterinburg.hh.ru/'
URL = 'https://ekaterinburg.hh.ru/search/vacancy/'
HEADERS = {
    'accept': 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
              '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/95.0.4638.54 Safari/537.36 '
}


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    vacancy = []
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='vacancy-serp-item vacancy-serp-item_premium vacancy-serp-item_tempexp-14189')

    for item in items:
        vacancy.append(
            {
             'vacancy_name': item.find('div', class_='vacancy-serp-item__info').get_text(strip=True),
             'vacancy_compensation': item.find('div', class_='vacancy-serp-item__sidebar').get_text(strip=True),
             'vacancy_page_link': item.find('div', class_='g-user-content').find('a').get('href')

            }
        )
    return vacancy


def data_save(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Вакансия', 'Зарплата', 'Ссылка на вакансию'])
        for item in items:
            writer.writerow([item['vacancy_name'], item['vacancy_compensation'], item['vacancy_page_link']])


def parser():
    PAGENATION = int(input('Количество страниц парсинга: ')).strip()
    html = get_html(URL)
    if html.status_code == 200:
        vacancy = []
        for page in range(1, PAGENATION+1):
            print(f'В процессе страница {page}')
            html = get_html(URL, params={'page': page})
            vacancy.extend(get_content(html.text))
            data_save(vacancy, CSV)
    else:
        print('Error')


parser()
        
