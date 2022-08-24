import requests
from bs4 import BeautifulSoup
import time
import os
from dotenv import load_dotenv



load_dotenv()
login = os.getenv('login')
password = os.getenv('password')
p = os.getenv('p')

url_mygkh = "https://my-gkh.ru/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.132 YaBrowser/22.3.1.892 Yowser/2.5 Safari/537.36'}
region_list = ['Белгородская область', 'Брянская область', 'Владимирская область', 'Воронежская область', 'Ивановская область', 'Калужская область', 'Костромская область', 'Курская область', 'Липецкая область', 'Москва', 'Московская область', 'Орловская область', 'Рязанская область', 'Смоленская область', 'Тамбовская область', 'Тверская область', 'Тульская область', 'Ярославская область', 'Архангельская область', 'Вологодская область', 'Карелия Республика', 'Коми Республика', 'Ленинградская область', 'Мурманская область', 'Новгородская область', 'Псковская область', 'Санкт-Петербург', 'Астраханская область', 'Волгоградская область', 'Краснодарский край', 'Ростовская область', 'Республика Крым', 'Севастополь', 'Башкортостан Республика', 'Кировская область', 'Марий Эл Республика', 'Мордовия Республика', 'Нижегородская область', 'Пензенская область', 'Самарская область', 'Саратовская область', 'Татарстан Республика', 'Удмуртская Республика', 'Ульяновская область', 'Чувашская Республика - Чувашия', 'Свердловская область', 'Курская область', 'Тюменская область', 'Челябинская область']
proxies = {
    'https': f'http://{login}:{password}@{p}'
}


# достаёт html text страницы
def get_html(website):
    counter = 0
    try:
        html_website = requests.get(website, headers=headers, proxies=proxies, timeout=60)
    except requests.exceptions.ProxyError:
        print(f'ProxyError: {counter}')
        time.sleep(10)
        for i in range(100):
            try:
                html_website = requests.get(website, headers=headers, proxies=proxies, timeout=27)
                break
            except requests.exceptions.ProxyError:
                counter = counter + 1
                print(f'ProxyError: {counter}')
                time.sleep(10)
                continue
    except requests.exceptions.ConnectTimeout:
        print(f'ConnectTimeout: {counter}')
        time.sleep(5)
        for i in range(100):
            try:
                html_website = requests.get(website, headers=headers, proxies=proxies, timeout=27)
                break
            except requests.exceptions.ConnectTimeout:
                time.sleep(10)
                counter = counter + 1
                print(f'ConnectTimeout: {counter}')
                continue
    except requests.exceptions.ReadTimeout:
        time.sleep(5)
        for i in range(100):
            print(f'ConnectTimeout: {counter}')
            try:
                html_website = requests.get(website, headers=headers, proxies=proxies, timeout=27)
                break
            except requests.exceptions.ReadTimeout:
                time.sleep(10)
                counter = counter + 1
                print(f'ConnectTimeout: {counter}')
                continue

    return html_website.text


########## узнать свой айпи ############
def get_location(url):
    response = requests.get(url=url, headers=headers, proxies=proxies)
    soup = BeautifulSoup(response.text, 'lxml')

    ip = soup.find('div', class_='ip').text.strip()
    location = soup.find('div', class_='value-country').text.strip()

    print(f'IP: {ip}\nLocation: {location}')


def get_ip():
    get_location(url='https://2ip.ru')

get_ip()
