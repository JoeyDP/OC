import bacli

from jinja2 import Environment, FileSystemLoader, select_autoescape


from course import *
from year import *


env = Environment(
    loader=FileSystemLoader('templates/'),
    autoescape=select_autoescape(['dot'])
)
template = env.get_template('template.dot')

OUTPUT = "output.dot"


@bacli.command
def run():
    with open(OUTPUT, 'w') as f:
        content = template.render(years=[year1, year2, year3])
        f.write(content)
