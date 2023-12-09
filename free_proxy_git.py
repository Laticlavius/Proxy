import asyncio
import aiohttp
import aiofiles
import re
import json

url_list = ["https://github.com/TheSpeedX/PROXY-List/blob/master/socks5.txt", 
            "https://github.com/TheSpeedX/PROXY-List/blob/master/socks4.txt",
            "https://github.com/TheSpeedX/PROXY-List/blob/master/http.txt",
            "https://github.com/ErcinDedeoglu/proxies/blob/main/proxies/http.txt",
            "https://github.com/ErcinDedeoglu/proxies/blob/main/proxies/https.txt",
            "https://github.com/ErcinDedeoglu/proxies/blob/main/proxies/socks4.txt",
            "https://github.com/ErcinDedeoglu/proxies/blob/main/proxies/socks5.txt"]

EXP = '\/(\w+.\w+$)'

async def writer(name, val):
    async with aiofiles.open(f'proxys/{name}', 'a', encoding='utf-8') as file:
        await file.write(f'{val}\n')



async def get_proxy(session, url):
    async with session.get(url) as response:
        resp = await response.read()
    hashrate = json.loads(resp)
    name = re.findall(EXP, url)[0]
    for item in hashrate['payload']['blob']['rawLines']:
        await writer(name, item)





async def gather():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in url_list:
            task = asyncio.create_task(get_proxy(session, url))
            tasks.append(task)
        await asyncio.gather(*tasks)



def main():
    asyncio.run(gather())


if __name__ == "__main__":
    main()