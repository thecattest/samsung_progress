from secret import USERNAME, PASSWORD
from elements import Module
from config import FIRST, SECOND, THIRD, FOURTH, FIFTH, PROJECT
import generate_html
import session

import asyncio
import time


async def main():
    s = await session.get(USERNAME, PASSWORD)

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


if __name__ == '__main__':
    start = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
    end = time.time()
    print(end - start)
