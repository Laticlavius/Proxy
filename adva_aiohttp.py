from bs4 import BeautifulSoup as bs
import re
import base64
import csv
import asyncio
import aiohttp

cookies = {
    '_ym_uid': '1700723349197591994',
    '_ym_d': '1700723349',
    '_ym_isad': '1',
    '_ym_visorc': 'w',
    '_ga': 'GA1.2.1098053931.1700723349',
    '_gid': 'GA1.2.1036490704.1700723349',
    'supportOnlineTalkID': 'OTZTDuP15N9TuaU5M2lOLWPgTIxi5WRP',
    'XSRF-TOKEN': 'eyJpdiI6IllXSXQ4eER3YzhteXVZZkpWRlBDT3c9PSIsInZhbHVlIjoiUnNuRWJZT3lidnB4SWlPMEUwSE9ZM2NLSVNPUUdmTWdyNEU3RHh2Y1NTTWE3K3lkaXVCR2RTRHdDVDJTc1A3bG1kTURwakFZUXg3b0MyZXVKV0c5Z2c9PSIsIm1hYyI6IjIzMWMwN2YxNGQwZWU3OWIyYmY1ZjE0MDJjY2Y5NWI3ODhhMDc5MTg3Y2Y2N2QxMmUyNzE2YTI2MjE3MWM3Y2QifQ%3D%3D',
    'laravel_session': 'eyJpdiI6IlVENmticnBQbU9xaFlPMlVnWUZmcWc9PSIsInZhbHVlIjoiZXdLaWE1MkVseW1mbDBua2dGeWY2cFdySHZLQTUybVVaNWEwOElMRHd2Y3dKQTNQczYxWm9wVXVTQ0JMZWVRWFRJRmRtWHFmWFdVTkFFd0dCcWxDVHc9PSIsIm1hYyI6ImRjZWUxYWUxMTIwMTJlZWJiOTJiOTllYTI3NGE2ZGVjMTA0ZGYyZTFlODg1OGJhNTZhNWQ4M2RmMzZmMTAxMzMifQ%3D%3D',
    '_ga_BQ8X8FM368': 'GS1.2.1700723349.1.1.1700723372.0.0.0',
}


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Cookie': '_ym_uid=1700723349197591994; _ym_d=1700723349; _ym_isad=1; _ym_visorc=w; _ga=GA1.2.1098053931.1700723349; _gid=GA1.2.1036490704.1700723349; supportOnlineTalkID=OTZTDuP15N9TuaU5M2lOLWPgTIxi5WRP; XSRF-TOKEN=eyJpdiI6IllXSXQ4eER3YzhteXVZZkpWRlBDT3c9PSIsInZhbHVlIjoiUnNuRWJZT3lidnB4SWlPMEUwSE9ZM2NLSVNPUUdmTWdyNEU3RHh2Y1NTTWE3K3lkaXVCR2RTRHdDVDJTc1A3bG1kTURwakFZUXg3b0MyZXVKV0c5Z2c9PSIsIm1hYyI6IjIzMWMwN2YxNGQwZWU3OWIyYmY1ZjE0MDJjY2Y5NWI3ODhhMDc5MTg3Y2Y2N2QxMmUyNzE2YTI2MjE3MWM3Y2QifQ%3D%3D; laravel_session=eyJpdiI6IlVENmticnBQbU9xaFlPMlVnWUZmcWc9PSIsInZhbHVlIjoiZXdLaWE1MkVseW1mbDBua2dGeWY2cFdySHZLQTUybVVaNWEwOElMRHd2Y3dKQTNQczYxWm9wVXVTQ0JMZWVRWFRJRmRtWHFmWFdVTkFFd0dCcWxDVHc9PSIsIm1hYyI6ImRjZWUxYWUxMTIwMTJlZWJiOTJiOTllYTI3NGE2ZGVjMTA0ZGYyZTFlODg1OGJhNTZhNWQ4M2RmMzZmMTAxMzMifQ%3D%3D; _ga_BQ8X8FM368=GS1.2.1700723349.1.1.1700723372.0.0.0',
    'Referer': 'https://www.google.ru/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

def create_csv():
    with open("result.csv", "w", encoding="utf-8", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(("ip", "port", "prot","country"))

create_csv()


async def get_page_data(session, page):
        
        params = {
            'page': page,
        }
        async with session.get('https://advanced.name/ru/freeproxy', cookies=cookies,headers=headers,params=params) as response:
            resp = await response.text()
            soup = bs(resp, 'html.parser')
            tr = soup.find('table', {'id': "table_proxies"}).find('tbody').find_all('tr')

            for td in tr:
                try:
                    ip = td.find('td', attrs={'data-ip': True}).get('data-ip')
                    decoded_ip = base64.b64decode(ip).decode('utf-8')
                    port = td.find('td', attrs={'data-port': True}).get('data-port')
                    decoded_port = base64.b64decode(port).decode('utf-8')
                    img = td.find_all('a')
                    prot = img[0].text
                    country = (img[-1:])[0].text
                except Exception as _ex:
                    print(_ex)
                    continue
                else:
                     with open("result.csv", "a", encoding="utf-8", newline='') as file:
                         writer = csv.writer(file)
                         writer.writerow(([decoded_ip, decoded_port, prot, country]))

async def gather():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://advanced.name/ru/freeproxy', cookies=cookies, headers=headers) as response:
            resp = await response.text()
            soup = bs(resp, 'html.parser')
            pages = soup.find('ul', {'class': 'pagination pagination-lg'}).find_all('li')
            pages = max([int(i.find('a').text) for i in pages if (i.find('a').text).isdigit()])

            tasks = []

            for page in range(1, pages + 1):
                task = asyncio.create_task(get_page_data(session, page))
                tasks.append(task)

            await asyncio.gather(*tasks)


def main():
    asyncio.run(gather())

if __name__ == "__main__":
    main()