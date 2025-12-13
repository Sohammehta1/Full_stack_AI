import asyncio
import aiohttp

async def fetch_url(session: aiohttp.ClientSession, url):
    async with session.get(url) as response:
        print(response.status)
        resp_text = await response.text() 
        print(resp_text[:15])

async def main():
    async with aiohttp.ClientSession() as session:
        tasks =  [fetch_url(session,url="https://youtube.com") for _ in range(3)]
        await asyncio.gather(*tasks) # '*' is used to unpack all the values in the iterator
asyncio.run(main())