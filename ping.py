from aiohttp import ClientProxyConnectionError, ClientConnectorCertificateError, ClientConnectorError, ClientHttpProxyError
import aiohttp
import asyncio


tasks = []

async def google_index_checker(sem):

    async with sem:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://127.0.0.1:8000/cities') as response_google:
                html_code = await response_google.text()
                print(html_code, sem)

async def main():
    global tasks
    sem = asyncio.Semaphore(500)
    for _ in range(100000):
        task = asyncio.Task(google_index_checker(sem))
        tasks.append(task)

    await asyncio.gather(*tasks)


if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
