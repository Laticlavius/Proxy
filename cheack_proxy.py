import requests
import time 
from bs4 import BeautifulSoup as bs
import re

cookies = {
    'PHPSESSID': 'g0q2ruhf6p45dh151gq02232u3',
    'ipHistory': '1700896408%2C1599000844',
    '_gid': 'GA1.2.415539232.1700896410',
    '_ga_KCM13JPWZR': 'GS1.1.1700896409.1.1.1700896658.0.0.0',
    '_ga': 'GA1.2.501871203.1700896410',
    '_gat_gtag_UA_5564916_1': '1',
}

headers = {
    'authority': '2ip.ru',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    # 'cookie': 'PHPSESSID=g0q2ruhf6p45dh151gq02232u3; ipHistory=1700896408%2C1599000844; _gid=GA1.2.415539232.1700896410; _ga_KCM13JPWZR=GS1.1.1700896409.1.1.1700896658.0.0.0; _ga=GA1.2.501871203.1700896410; _gat_gtag_UA_5564916_1=1',
    'referer': 'https://www.google.ru/',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-full-version-list': '"Google Chrome";v="119.0.6045.160", "Chromium";v="119.0.6045.160", "Not?A_Brand";v="24.0.0.0"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"15.0.0"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}


proxies = {
    'http': 'http://23.145.80.66:4128',
    'https': 'http://23.145.80.66:4128'
}

response = requests.get('https://2ip.ru/', proxies=proxies)
start_time = time.perf_counter()
# with open('index.html', 'w',  encoding="utf-8") as file:
#     file.write(response.text)

# with open('index.html', 'r', encoding='utf-8') as file:
#     index = file.read()



# soup = bs(index, 'html.parser')
soup = bs(response.text, 'html.parser')

ip = soup.find('div',{'class': "ip-info_left"}).find('div',{'class': 'ip'}).find('span').text

counry = soup.find('div', {'class': 'data_table'}).find('div', {'id': 'ip-info-country'}).text

pattern = r'[А-Яа-я]+,'
counry  = re.findall(pattern, counry)[0][:-1]

pattern_2 = r'([а-яА-Я]+) ([а-яА-Я]+)'
use_proxy = soup.find('div', {'class': 'data_table'}).find_all('div', {'class':'data_item'})[-2:-1]
lst = [cls.get('class') for i in use_proxy for cls in i.find_all('div')][1][0]
cls_prox = [i.find('div', {'class': lst}).text for i in use_proxy]
use_1  = re.findall(pattern_2,cls_prox[0])[0]
use_1 = ' '.join(use_1) 

protection = soup.find('div', {'class': 'data_table'}).find_all('div', {'class':'data_item'})[-1:]
lst_p = [cls.get('class') for i in protection for cls in i.find_all('div')][1][0]
cls_prot = [i.find('div', {'class': lst}).text for i in protection]

use_2  = cls_prot[0].strip().split('\n')[0]




print(ip,counry,use_1,use_2)
