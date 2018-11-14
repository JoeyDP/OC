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

OUTPUT_DIR = "output/"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def getOutputPath(filename):
    return os.path.join(OUTPUT_DIR, filename)


@bacli.command
def current(noWorkload: bool=False):
    template = env.get_template('normal.dot')
    output = getOutputPath("current.dot")
    render(template, output, includeWorkload=not noWorkload)


@bacli.command
def solution(noWorkload: bool=False):
    doSolution()
    template = env.get_template('normal.dot')
    output = getOutputPath("solution_abs.dot")
    render(template, output, includeWorkload=not noWorkload, absolute=True)
    output = getOutputPath("solution_rel.dot")
    render(template, output, includeWorkload=not noWorkload, absolute=False)


@bacli.command
def per_course(noWorkload: bool=False):
    # courses = [c for y in YEARS for c in y.courses]
    courses = [GP]
    for course in courses:
        os.makedirs(getOutputPath(course.id), exist_ok=True)
        template = env.get_template('normal.dot')
        output = getOutputPath(os.path.join(course.id, "current.dot"))
        render(template, output, includeWorkload=not noWorkload, highlightCourse=course)

    doSolution()
    for course in courses:
        template = env.get_template('normal.dot')
        output = getOutputPath(os.path.join(course.id, "solution_abs.dot"))
        render(template, output, includeWorkload=not noWorkload, absolute=True, highlightCourse=course)
        output = getOutputPath(os.path.join(course.id, "solution_rel.dot"))
        render(template, output, includeWorkload=not noWorkload, absolute=False, highlightCourse=course)


def doSolution():
    # GP
    GP.getDependency(CG).remove()
    GP.getDependency(PSE).remove()

    # MB
    MB.addNewDependency(IP)

    # WP
    WP.getDependency(GP).remove()

    # SE
    SE.getDependency(IDBS).remove()
    SE.getDependency(PPD).remove()
    SE.getDependency(GAS).remove()
    SE.getDependency(TA).remove()

    # DS
    DS.getDependency(GP).remove()
    DS.addNewDependency(IDBS)

    # AI
    AI.getDependency(AC).remove()

    # DSGA
    DSGA.addNewDependency(AC, soft=True)

    # COMP
    COMP.addNewDependency(GP)
    COMP.addNewDependency(MB)
    COMP.getDependency(CSA).remove()
    COMP.getDependency(TA).remove()
    COMP.getDependency(GAS).remove()

    # BAE
    BAE.getDependency(GP).setSoft(True)
    BAE.getDependency(PPD).setSoft(True)


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
