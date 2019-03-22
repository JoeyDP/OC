import os
import shutil
from collections import defaultdict
import bacli

from jinja2 import Environment, FileSystemLoader, select_autoescape
import pydot
from tqdm import tqdm

import program.course
from program.arch import *
from program.simulator import Simulator


env = Environment(
    loader=FileSystemLoader('templates/'),
    autoescape=select_autoescape(['dot']),
    trim_blocks=True,
    lstrip_blocks=True,
)


YEARS = [year1, year2, year3]


def getCourses():
    return [c for y in YEARS for c in y.courses]


OUTPUT_DIR = "output/arch/"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def getOutputPath(filename):
    return os.path.join(OUTPUT_DIR, filename)


@bacli.command
def current(fullnames: bool = False):
    """ Generate the current program. """
    program.course.FULL_NAMES = fullnames

    for course in getCourses():
        course.validate()

    template = env.get_template('normal.dot')
    output = getOutputPath("current.dot")
    renderDot(template, output, title="Origineel", includeWorkload=False, fullnames=fullnames)


@bacli.command
def legend():
    """ Generate the legend. """
    template = env.get_template('legend.dot')
    output = getOutputPath("legend.dot")
    renderDot(template, output, courses=getCourses())


@bacli.command
def simulate(failures: int = 1):
    courses = getCourses()
    electives = []
    electiveCredits = 0
    for elective in electives:
        courses.remove(elective)
        electiveCredits += elective.sp
    s = Simulator(YEARS, courses, electiveCredits)
    s.simulate(nrFailures=failures)


def toPdf(inpath, outpath=None):
    if outpath is None:
        outpath = toExtension(inpath, ".pdf")
    (graph,) = pydot.graph_from_dot_file(inpath)
    graph.write_pdf(outpath)


def renderTemplate(template, output, **kwargs):
    with open(output, 'w') as f:
        content = template.render(**kwargs)
        f.write(content)


def renderDot(template, output, **kwargs):
    templateArgs = {
        'years': YEARS,
        'teachers': Teacher.all,
        'absolute': True
    }
    templateArgs.update(kwargs)
    renderTemplate(template, output, **templateArgs)
    toPdf(output)


def toExtension(p, ext):
    return os.path.splitext(p)[0] + ext
