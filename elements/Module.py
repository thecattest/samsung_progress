from bs4 import BeautifulSoup as bs
from elements.Book import Book
from elements.Assign import Assign
from elements.Test import Test
import asyncio


class Module:
    def __init__(self, session, section_id):
        self.session = session
        self.section = section_id
        self.link = ""
        self.bs = None
        self.title = ""

        self.books = []
        self.tasks = []
        self.assigns = []
        self.tests = []

        self.tests_done = self.assigns_done = 0

    async def load(self):
        module_link = "https://myitschool.ru/edu/course/view.php"
        params = {
            "id": 6,
            "section": self.section
        }
        response = await self.session.get(module_link, params=params)
        module_bs = bs(await response.text(), "html.parser")
        self.link = str(response.url)
        self.bs = module_bs
        self.title = self.bs.select_one("div.section-navigation.navigationtitle h3.sectionname span").text

        self.books = self.load_books()
        self.tasks = await self.load_tasks()

        self.tests_done = len(list(filter(lambda x: x.done, self.tests)))
        self.assigns_done = len(list(filter(lambda x: x.done, self.assigns)))

        return self

    def load_books(self):
        books = self.bs.select("li.activity.book.modtype_book")
        books = [Book(b.attrs["id"], b.find("a").attrs["href"],
                      b.span.text.replace("Книга", "").strip())
                 for b in books]
        return sorted(books, key=lambda b: b.id)

    def print_books(self):
        string = ""
        for book in self.books:
            string += str(book) + "\n"
        return string

    async def load_tasks(self):
        tasks = await asyncio.gather(self.load_assigns(), self.load_tests())
        self.assigns = tasks[0]
        self.tests = tasks[1]
        tasks = tasks[0] + tasks[1]

        return sorted(tasks, key=lambda t: t.id)

    async def load_assigns(self):
        assign = self.bs.select(".activity.assign.modtype_assign")
        assign = [Assign(self.session, t.attrs["id"], t.find("a").attrs["href"],
                         t.span.text.strip())
                  for t in assign]
        assign = await asyncio.gather(*[a.load() for a in assign])
        return assign

    async def load_tests(self):
        quiz = self.bs.select(".activity.quiz.modtype_quiz")
        quiz = [Test(self.session, t.attrs["id"], t.find("a").attrs["href"],
                     t.span.text.replace(" Тест", "").strip())
                for t in quiz]
        quiz = await asyncio.gather(*[q.load() for q in quiz])
        return quiz

    def print_tasks(self):
        string = ""
        for task in self.tasks:
            string += str(task) + "\n"
        return string

    def __str__(self):
        string = self.title + " " + self.link
        string += "\n\n==============================\n"
        string += self.print_books()
        string += "\n==============================\n"
        string += self.print_tasks()
        return string
