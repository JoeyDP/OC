import os
import bacli

from jinja2 import Environment, FileSystemLoader, select_autoescape
import pydot
from tqdm import tqdm

from program.course import *
from program.year import *
from program.teacher import *

env = Environment(
    loader=FileSystemLoader('templates/'),
    autoescape=select_autoescape(['dot']),
    trim_blocks=True,
    lstrip_blocks=True,
)


YEARS = [year1, year2, year3]


def getCourses():
    return [c for y in YEARS for c in y.courses]


OUTPUT_DIR = "output/"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def getOutputPath(filename):
    return os.path.join(OUTPUT_DIR, filename)


@bacli.command
def current(workload: bool=False):
    """ Generate the current program. """
    template = env.get_template('normal.dot')
    output = getOutputPath("current.dot")
    render(template, output, title="Origineel", includeWorkload=workload)


@bacli.command
def solution(workload: bool=False):
    """ Generate solution 1 with absolute and relative visualization. """
    doSolution()

    template = env.get_template('normal.dot')
    output = getOutputPath("solution_abs.dot")
    render(template, output, title="Voortstel", includeWorkload=workload, absolute=True)
    output = getOutputPath("solution_rel.dot")
    render(template, output, title="Voortstel (Relatief)", includeWorkload=workload, absolute=False)


@bacli.command
def per_course(workload: bool=False):
    """ Generate solution 1 per course (with highlighting). """
    courses = getCourses()

    with tqdm(total=2) as pbar:
        for course in tqdm(courses):
            os.makedirs(getOutputPath(course.id), exist_ok=True)
            template = env.get_template('normal.dot')
            output = getOutputPath(os.path.join(course.id, "current.dot"))
            render(template, output, title="Origineel {}".format(course.shortName), includeWorkload=workload, highlightCourse=course)

        pbar.update()
        doSolution()
        for course in tqdm(courses):
            template = env.get_template('normal.dot')
            output = getOutputPath(os.path.join(course.id, "solution_abs.dot"))
            render(template, output, title="Voortstel {}".format(course.shortName), includeWorkload=workload, absolute=True, highlightCourse=course)
            output = getOutputPath(os.path.join(course.id, "solution_rel.dot"))
            render(template, output, title="Voortstel {} (Relatief)".format(course.shortName), includeWorkload=workload, absolute=False, highlightCourse=course)


@bacli.command
def per_teacher(workload: bool=False):
        with tqdm(total=2) as pbar:
            for teacher in tqdm(Teacher.all):
                for course in tqdm(teacher.courses):
                    outputPath = getOutputPath(os.path.join(teacher.fullName, course.id))
                    os.makedirs(outputPath, exist_ok=True)
                    template = env.get_template('normal.dot')
                    output = os.path.join(outputPath, "current.dot")
                    render(template, output, title="Origineel {}".format(course.shortName), includeWorkload=workload, highlightCourse=course)

            pbar.update()
            doSolution()
            for teacher in tqdm(Teacher.all):
                for course in tqdm(teacher.courses):
                    outputPath = getOutputPath(os.path.join(teacher.fullName, course.id))
                    template = env.get_template('normal.dot')
                    output = os.path.join(outputPath, "solution_abs.dot")
                    render(template, output, title="Voortstel {}".format(course.shortName), includeWorkload=workload, absolute=True, highlightCourse=course)
                    output = os.path.join(outputPath, "solution_rel.dot")
                    render(template, output, title="Voortstel {} (Relatief)".format(course.shortName), includeWorkload=workload, absolute=False, highlightCourse=course)


@bacli.command
def legend():
    """ Generate the legend. """
    template = env.get_template('legend.dot')
    output = getOutputPath("legend.dot")
    render(template, output, courses=getCourses())


def doSolution():
    doSolutionDep()
    doSolutionCourses()

    for course in getCourses():
        course.validate()


def doSolutionDep():
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
    SE.addNewDependency(PSE)

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


def doSolutionCourses():
    # move courses
    US.moveTo(year2.semester2)
    AC.moveTo(year2.semester1)

    AI.moveTo(year2.semester1)
    AC.moveTo(year3.semester1)


@bacli.command
def experiment(noWorkload: bool=False):
    """ Use this command to experiment with changes. """
    doSolutionDep()

    # move courses
    US.moveTo(year2.semester2)
    AC.moveTo(year2.semester1)

    # TODO: In first proposition?
    IDBS.getDependency(GAS).setSoft(True)
    IDBS.moveTo(year1.semester2)
    PSE.moveTo(year2.semester2)
    PPD.moveTo(year2.semester1)

    # AI.moveTo(year2.semester2)
    AC.moveTo(year3.semester1)

    CN.moveTo(year2.semester1)
    TCS.moveTo(year2.semester2)
    TCS.getDependency(GP).setSoft(True)
    TCS.getDependency(CN).setSoft(True)

    # TODO: In first proposition?
    # COMP.getDependency(GP).setSoft(True)
    # COMP.getDependency(MB).setSoft(True)
    # COMP.moveTo(year2.semester2)

    for course in getCourses():
        course.validate()

    # render
    template = env.get_template('normal.dot')
    output = getOutputPath("solution3_abs.dot")
    render(template, output, includeWorkload=not noWorkload, absolute=True)
    output = getOutputPath("solution3_rel.dot")
    render(template, output, includeWorkload=not noWorkload, absolute=False)


def toPdf(inpath, outpath=None):
    if outpath is None:
        outpath = toExtension(inpath, ".pdf")
    (graph,) = pydot.graph_from_dot_file(inpath)
    graph.write_pdf(outpath)


def render(template, output, **kwargs):

    templateArgs = {
        'years': YEARS,
        'teachers': Teacher.all,
        'absolute': True
    }
    templateArgs.update(kwargs)

    with open(output, 'w') as f:
        content = template.render(**templateArgs)
        f.write(content)

    toPdf(output)


def toExtension(p, ext):
    return os.path.splitext(p)[0] + ext
