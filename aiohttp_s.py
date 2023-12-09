import aiofiles
import aiohttp
import asyncio
from aiohttp_socks import ProxyConnector


TEST_TIMEOUT = 200



async def test(url,prox):
     if len(prox) > 1:
        connector = ProxyConnector.from_url(f'socks5://{prox}', rdns=True)
        async with aiohttp.ClientSession(connector=connector) as session:
            
            try:
                async with session.get(url, proxy= f'http://{prox}',timeout=TEST_TIMEOUT) as response:
                    resp_json = await response.json()
                    
            except Exception as ex:
                pass
            
            else:
                if resp_json:
                            async with aiofiles.open('r.txt', 'a', encoding='utf-8') as file:
                                await file.write(f'{prox} - работает\n')


async def read_file_ip():
    async with aiofiles.open('proxys/socks5.txt', 'r', encoding='utf-8') as file:
        proxys = await file.read()

    return proxys.split('\n')
    

async def main():
    data = await read_file_ip()

    url = 'https://httpbin.org/ip'


    await asyncio.gather(*[test(url, proxy) for  proxy in data])


if __name__ == "__main__":
    asyncio.run(main())