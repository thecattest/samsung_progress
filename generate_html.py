import os
import glob
from jinja2 import Environment, FileSystemLoader


current_directory = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(current_directory))

templates = glob.glob('templates/*.html')


def render_template(filename):
    return env.get_template(filename).render(
        foo='Hello',
        bar='World'
    )


for f in templates:
    print(f)
    rendered_string = render_template(f)
    print(rendered_string)
