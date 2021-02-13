from elements.Material import Material
from bs4 import BeautifulSoup as bs


class Assign(Material):
    def __init__(self, session, assign_id, link, title):
        super().__init__(assign_id, link, title)
        self.session = session
        self.assign_page = None
        self.done = True
        self.points_repr = ""

    async def load(self):
        # print(self.link + " started")
        response = await self.session.get(self.link)
        # print(self.link + " finished")
        self.assign_page = bs(await response.text(), features="html.parser")
        res_cell = self.assign_page.select(".submissionstatussubmitted")
        self.done = bool(len(res_cell))
        self.points_repr = 'ok' if self.done else '*'
        return self

    def __str__(self):
        return f"<Assign {self.points_repr}> " + super().__str__()
