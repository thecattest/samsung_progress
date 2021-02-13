import os
from jinja2 import Environment, FileSystemLoader


current_directory = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(current_directory))


def render_template(modules):
    return env.get_template("templates/index.html").render(
        modules=modules
    )
