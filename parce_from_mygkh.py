from bs4 import BeautifulSoup
import time
from config import get_html, url_mygkh, region_list
from random import randint



# достаёт url региона/области/города/республики и кладём в список
def get_url_region_list():
    html = get_html(url_mygkh)
    url_region_list = []
    soup = BeautifulSoup(html, 'html.parser')
    for region_name in region_list:
        for link in soup.find_all('a', href=True, text=region_name):
            url_region = url_mygkh + link["href"]
            url_region_list.append(url_region)
    print('url_region_list ready', type(url_region_list), len(url_region_list))
    return url_region_list


# собираем список всех url-адресов ук
def get_url_managing_companise_list():
    url_managing_companise_list = []
    url_region_list = get_url_region_list()
    n = 1
    for url_region in url_region_list:
        print(f'{url_region}', f'№ {n}')
        n = n + 1
        html= get_html(url_region)
        soup = BeautifulSoup(html, 'html.parser')
        time.sleep(1)

        # узнаём скока страниц ук в регионе
        for link in soup.find_all('a', href=True, text='»»'):

            l = str(link["href"]).split("=")
            pages = l[-1]
            print("страниц ук в регионе ", pages) # количество стр
            # time.sleep(1)
            # собираем список всех url-адресов ук на странице и листаем далее
            for page in range(int(pages)):
                p = page + 1
                url_mc_page = url_region + "?page=" +str(p)
                html = get_html(url_mc_page)
                soup = BeautifulSoup(html, 'html.parser')
                for link in soup.find_all('a', href=True):
                    if "/getorganization/" in link["href"]:
                        url_managing_companise = url_mygkh + link["href"]
                        url_managing_companise_list.append(url_managing_companise)

                time.sleep(2.5)
                print('длинна url_managing_companise_list ', len(url_managing_companise_list))
    print('url_managing_companise_list done')
    return url_managing_companise_list


# парсер отдаёт список со словорями в которых лежит информация по компаниям. ключ - Полное наименование, Сокращенное наименование и т.д - значение data
def parce():
    url_managing_companise_list = get_url_managing_companise_list()
    dic_mc_list = []
    counter = 1
    for url_managing_companise in url_managing_companise_list:
        html= get_html(url_managing_companise)
        soup = BeautifulSoup(html, 'html.parser')


        dic_mc = {}
        headlines = []
        data = []
        dic_mc2 = {}
        headlines2 = []
        data2 = []

        # собираем заголовки и data в левой колонке и кладём их в словарь
        for headlines_1 in soup.find_all('h4', {"class": "text-color"}):
            headlines.append(headlines_1.text)

        for data_1 in soup.find_all('p', {"class": "text-s"}):
            data.append(data_1.text)

        for i in range(len(headlines)):
            try:
                dic_mc[headlines[i]] = data[i]
            except:
                continue

        # собираем заголовки и data в правой колонке и кладём их в другой словарь, затем объединяем словари
        for headlines_2 in soup.find_all('b', {"class": "text-s"}):
            if headlines_2.text == 'Адрес организации на карте':
                break
            headlines2.append(headlines_2.text)

        for data_2 in soup.find_all('span', {"class": "text-s"}):
            data2.append(data_2.text)

        for i in range(len(headlines2)):
            try:
                dic_mc2[headlines2[i]] = data2[i]
            except:
                continue
        dic_mc.update(dic_mc2)

        dic_mc_list.append(dic_mc)
        time.sleep(2.5)
        try:
            print("counter ", counter, len(dic_mc_list), dic_mc['Руководитель организации'])
        except:
            try:
                print("counter ", counter, len(dic_mc_list), dic_mc['Почтовый адрес'])
            except:
                print("counter ", counter, len(dic_mc_list))
        counter = counter + 1
    print("dic_mc_list done")
    return dic_mc_list, #print(dic_mc_list, type(dic_mc_list))