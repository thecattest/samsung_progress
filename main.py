from secret import USERNAME, PASSWORD
from elements import Module
from config import *
import generate_html

import asyncio
import aiohttp

from bs4 import BeautifulSoup as bs

import time


async def get_session(user, passw, save=True, filename='.session'):
    session = aiohttp.ClientSession()
    try:
        session.cookie_jar.load(filename)
        print("loaded")
        assert await is_session_alive(session)
        print("alive")
        return session
    except FileNotFoundError:
        pass
    except AssertionError:
        print("not alive")

    login_page_link = "https://myitschool.ru/edu/login/index.php"
    data = {
        "username": user,
        "password": passw,
    }

    login_page_response = await session.get(login_page_link)
    login_page = bs(await login_page_response.text(), features="html.parser")
    data["logintoken"] = login_page.select("input[name=logintoken]")[0].attrs["value"]

    await session.post(login_page_link, data=data)
    if save:
        session.cookie_jar.save(filename)

    print("got")
    return session


async def is_session_alive(session):
    login_page_link = "https://myitschool.ru/edu/login/index.php"
    login_page_response = await session.get(login_page_link)
    login_page = bs(await login_page_response.text(), features="html.parser")
    return login_page.select("#loginerrormessage") == []


async def main():
    s = await get_session(USERNAME, PASSWORD)

    # module = Module(session=s, section_id=THIRD)
    # await module.load()
    # print(module)

    modules = [Module(s, i) for i in [FIRST, SECOND, THIRD, FOURTH, FIFTH]]
    modules = await asyncio.gather(*[m.load() for m in modules])

    # for i in [FIRST, SECOND, THIRD, FOURTH, FIFTH]:
    #     module = Module(session=s, section_id=i)
    #     await module.load()
    #     print(module)

    with open("res.html", "wt") as file:
        file.write(generate_html.render_template(modules))
    await s.close()

start = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
end = time.time()
print(end - start)
