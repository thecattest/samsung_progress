from elements.Material import Material
from bs4 import BeautifulSoup as bs
import re
import asyncio


class Test(Material):
    def __init__(self, session, test_id, link, title):
        super().__init__(test_id, link, title)
        self.session = session
        self.test_page = None
        self.done = False
        self.points = 0.0
        self.max_points = 0.0
        self.attempts = []
        self.points_repr = ""
        # self.load()

    async def load(self):
        print(self.link + " started")
        response = await self.session.get(self.link)
        print(self.link + " finished")
        self.test_page = bs(await response.text(), features="html.parser")
        feedback = self.test_page.select("#feedback")
        if feedback:
            self.done = True

            feedback = feedback[0]
            points = re.findall(r"\d{1,2},\d\d\s?/\s?\d{1,2},\d\d", feedback.h3.text)[0].replace(",", ".")
            self.points = float(points.split("/")[0])
        else:
            self.done = False
        table = self.test_page.select("table.quizattemptsummary")
        if table:
            table = table[0]
            try:
                res_col = table.select("th.c3")[0]
                self.max_points = float(res_col.text.split("/")[1].replace(",", "."))
            except (IndexError, ValueError):
                try:
                    res_col = table.select("th.c2")[0]
                    self.max_points = float(res_col.text.split("/")[1].replace(",", "."))
                except IndexError:
                    self.max_points = 0.0
            self.attempts = [Attempt(tr, self.max_points)
                             for tr in table.select("tbody tr")]

        self.points_repr = str(self.points) + "/" + str(self.max_points) if self.attempts else "*"
        return self

    def __str__(self):
        string = "<Test " + self.points_repr + "> " + super().__str__()
        for at in self.attempts:
            string += "\n" + str(at)
        return string


class Attempt:
    def __init__(self, tr, max_points):
        if "процесс" not in tr.select("td.c1")[0].text:
            self.finished = True
            try:
                self.points = float(tr.select("td.c3")[0].text.replace(",", "."))
            except ValueError:
                self.points = float(tr.select("td.c2")[0].text.replace(",", "."))
            self.link = tr.select("a")[0].attrs["href"]
        else:
            self.finished = False
            self.link = ""
        self.max_points = max_points

    def __str__(self):
        points = str(self.points) + "/" + str(self.max_points) if self.finished else "*"
        return "\t<Attempt " + points + "> " + self.link
