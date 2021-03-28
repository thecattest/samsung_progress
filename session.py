import aiohttp


async def get(user, passw, save=True, filename='.session'):
    session = aiohttp.ClientSession()
    try:
        session.cookie_jar.load(filename)
        print("loaded session")
        assert await is_session_alive(session)
        print("session is alive")
        return session
    except FileNotFoundError:
        pass
    except AssertionError:
        print("session is not alive")

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

    print("got new session")
    return session


async def is_alive(session):
    login_page_link = "https://myitschool.ru/edu/login/index.php"
    login_page_response = await session.get(login_page_link)
    login_page = bs(await login_page_response.text(), features="html.parser")
    return login_page.select("#loginerrormessage") == []
