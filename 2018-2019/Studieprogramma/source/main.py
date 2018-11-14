import os
import bacli

from jinja2 import Environment, FileSystemLoader, select_autoescape
import pydot

from course import *
from year import *


env = Environment(
    loader=FileSystemLoader('templates/'),
    autoescape=select_autoescape(['dot']),
    trim_blocks=True,
    lstrip_blocks=True,
)


YEARS = [year1, year2, year3]


@bacli.command
def current(noWorkload: bool=False):
    template = env.get_template('normal.dot')
    output = "current.dot"
    render(template, output, includeWorkload=not noWorkload)


@bacli.command
def solution(noWorkload: bool=False):
    GP.getDependency(CG).remove()

    template = env.get_template('normal.dot')
    output = "solution_abs.dot"
    render(template, output, includeWorkload=not noWorkload, absolute=True)
    output = "solution_rel.dot"
    render(template, output, includeWorkload=not noWorkload, absolute=False)


def render(template, output, **kwargs):

    templateArgs = {
        'years': YEARS,
        'absolute': True
    }
    templateArgs.update(kwargs)

    with open(output, 'w') as f:
        content = template.render(**templateArgs)
        f.write(content)

    (graph,) = pydot.graph_from_dot_file(output)
    graph.write_pdf(toExtension(output, ".pdf"))


def toExtension(p, ext):
    return os.path.splitext(p)[0] + ext
