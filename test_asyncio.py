import aiohttp
import asyncio
from bs4 import BeautifulSoup as bs


async def load_task_info(task_id, s: aiohttp.ClientSession):
    response = await s.get("https://myitschool.ru/edu/mod/quiz/view.php",
                           params={
                               "id": task_id
                           })
    response.raise_for_status()
    print(f"Response status ({response.url}): {response.status}")
    print(bs(await response.text()))
    return 1
    # print(response_page.select("#feedback"))


async def main():
    ids = [
        563,
        567,
        568,
        573,
        563,
        567,
        568,
        563,
        567,
        568,
        563,
        567,
        568
    ]
    async with aiohttp.ClientSession() as session:
        res = await asyncio.gather(*[load_task_info(task_id, session) for task_id in ids])
        print(res)
        print(*dir(session.cookie_jar), sep='\n')
        print(session.cookie_jar.load())


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
