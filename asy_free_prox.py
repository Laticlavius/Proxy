from bs4 import BeautifulSoup as bs
import requests
import lxml
import re
import base64
import csv
import asyncio
import aiohttp

def create_csv():
    with open("result.csv", "w", encoding="utf-8", newline='') as file:

        writer = csv.writer(file)
        writer.writerow(("ip", "port", "prot","country"))

create_csv()

async def get_page_data(session, page):
    cookies = {
        '_ga': 'GA1.1.1594057476.1700557416',
        'fp': '754888e32f8e2ab67bc336d777876727',
        '_ga_FS4ESHM7K5': 'GS1.1.1700647044.2.1.1700647066.0.0.0',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie': '_ga=GA1.1.1594057476.1700557416; fp=754888e32f8e2ab67bc336d777876727; _ga_FS4ESHM7K5=GS1.1.1700647044.2.1.1700647066.0.0.0',
        'Referer': 'http://free-proxy.cz/ru/proxylist/country/RU/https/ping/all',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }

    async with session.get(f'http://free-proxy.cz/ru/proxylist/country/RU/all/ping/all/{page}',cookies=cookies,headers=headers) as response:
        resp = await response.text()
        soup = bs(resp, 'html.parser')
        proxys = soup.find('table', {'id': 'proxy_list'}).find('tbody').find_all('tr')

        for prox in proxys:
            try:
                    ip = prox.find('script').text
                    port = prox.find('span', {'class': 'fport'}).text
                    sm = prox.find_all('small')
                    prot = sm[0].text
                    country = prox.find('img').get('alt')
            except Exception as _ex:
                    continue
            else:
                    if ip:
                        pattern = r'\("([^"]*)"\)'
                        encoded_string  = re.findall(pattern, ip)[0]
                        decoded_ip = base64.b64decode(encoded_string).decode('utf-8')
                        with open("result.csv", "a", encoding="utf-8", newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(([decoded_ip, port, prot, country]))
        print(f"[INFO] : {page} --> download")



async def gather():
    
        cookies = {
        '_ga': 'GA1.1.1594057476.1700557416',
        'fp': '754888e32f8e2ab67bc336d777876727',
        '_ga_FS4ESHM7K5': 'GS1.1.1700647044.2.1.1700647066.0.0.0',
        }

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            # 'Cookie': '_ga=GA1.1.1594057476.1700557416; fp=754888e32f8e2ab67bc336d777876727; _ga_FS4ESHM7K5=GS1.1.1700647044.2.1.1700647066.0.0.0',
            'Referer': 'http://free-proxy.cz/ru/proxylist/country/RU/https/ping/all',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            }

        async with aiohttp.ClientSession() as session:
                    async with session.get('http://free-proxy.cz/ru/proxylist/country/RU/all/ping/all',cookies=cookies,headers=headers) as response:
                        resp = await response.text()
                    
                    

                        soup = bs(resp, 'html.parser')
                        max_pages = soup.find('div', {'class', 'paginator'}).find_all('a')
                        pages = max([int(i.text) for i in max_pages if (i.text).isdigit()])
                        tasks = []

                        for page in range(1, pages + 1):
                            task = asyncio.create_task(get_page_data(session, page))
                            tasks.append(task)

                        await asyncio.gather(*tasks)




def main():
    asyncio.run(gather())


if __name__ == "__main__":
    main()


