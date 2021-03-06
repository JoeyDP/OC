import os
import shutil
from collections import defaultdict
import bacli

from jinja2 import Environment, FileSystemLoader, select_autoescape
import pydot
from tqdm import tqdm

import program.course
from program.cs import *
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


OUTPUT_DIR = "output/cs/"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def getOutputPath(filename):
    return os.path.join(OUTPUT_DIR, filename)


@bacli.command
def current(fullnames: bool = False):
    """ Generate the current program. """
    program.course.FULL_NAMES = fullnames

    template = env.get_template('normal.dot')
    output = getOutputPath("current.dot")
    renderDot(template, output, title="Origineel", includeWorkload=True, fullnames=fullnames)


@bacli.command
def solution(fullnames: bool = False):
    """ Generate solution 1 with absolute and relative visualization. """
    program.course.FULL_NAMES = fullnames

    doSolution()

    template = env.get_template('normal.dot')
    output = getOutputPath("solution_abs.dot")
    renderDot(template, output, title="Voorstel", includeWorkload=True, absolute=True, fullnames=fullnames)
    output = getOutputPath("solution_rel.dot")
    renderDot(template, output, title="Voorstel (Relatief)", includeWorkload=True, absolute=False, fullnames=fullnames)


@bacli.command
def per_course(fullnames: bool = False):
    """ Generate solution 1 per course (with highlighting). """
    program.course.FULL_NAMES = fullnames

    courses = getCourses()

    with tqdm(total=2) as pbar:
        for course in tqdm(courses):
            os.makedirs(getOutputPath(course.id), exist_ok=True)
            template = env.get_template('normal.dot')
            output = getOutputPath(os.path.join(course.id, "current.dot"))
            renderDot(template, output, title="Origineel ({} gehighlight)".format(course.shortName), includeWorkload=True, highlightCourse=course, fullnames=fullnames)

        pbar.update()
        doSolution()
        for course in tqdm(courses):
            template = env.get_template('normal.dot')
            output = getOutputPath(os.path.join(course.id, "solution_abs.dot"))
            renderDot(template, output, title="Voorstel ({} gehighlight)".format(course.shortName), includeWorkload=True, absolute=True, highlightCourse=course, fullnames=fullnames)
            output = getOutputPath(os.path.join(course.id, "solution_rel.dot"))
            renderDot(template, output, title="Voorstel Relatief ({} gehighlight)".format(course.shortName), includeWorkload=True, absolute=False, highlightCourse=course, fullnames=fullnames)


@bacli.command
def per_teacher(fullnames: bool = False):
    program.course.FULL_NAMES = fullnames

    with tqdm(total=2) as pbar:
        for teacher in tqdm(Teacher.all):
            for course in tqdm(teacher.courses):
                outputPath = getOutputPath(os.path.join(teacher.fullName, course.id))
                os.makedirs(outputPath, exist_ok=True)
                template = env.get_template('normal.dot')
                output = os.path.join(outputPath, "current.dot")
                renderDot(template, output, title="Origineel ({} gehighlight)".format(course.shortName), includeWorkload=True, highlightCourse=course, fullnames=fullnames)

        pbar.update()
        doSolution()
        for teacher in tqdm(Teacher.all):
            teacherPath = getOutputPath(teacher.fullName)
            for course in tqdm(teacher.courses):
                outputPath = os.path.join(teacherPath, course.id)
                if not course.hasChanges():
                    tqdm.write("No changes in {}".format(course))
                    shutil.rmtree(outputPath)
                    continue
                template = env.get_template('normal.dot')
                output = os.path.join(outputPath, "solution_abs.dot")
                renderDot(template, output, title="Voorstel ({} gehighlight)".format(course.shortName), includeWorkload=True, absolute=True, highlightCourse=course, fullnames=fullnames)
                output = os.path.join(outputPath, "solution_rel.dot")
                renderDot(template, output, title="Voorstel Relatief ({} gehighlight)".format(course.shortName), includeWorkload=True, absolute=False, highlightCourse=course, fullnames=fullnames)

            if len(os.listdir(teacherPath)) == 0:
                tqdm.write("No changes for {}".format(teacher.fullName))
                # os.rmdir(teacherPath)
            # else:
            template = env.get_template('email.txt')
            output = os.path.join(teacherPath, "email.txt")
            renderTemplate(template, output, teacher=teacher)


@bacli.command
def legend():
    """ Generate the legend. """
    template = env.get_template('legend.dot')
    output = getOutputPath("legend.dot")
    renderDot(template, output, courses=getCourses())


@bacli.command
def changes(filter:str=None):
    """ Print all changes in text format """
    doSolution()
    changes = set()
    for course in getCourses():
        if filter is None or course.id == filter:
            changes.update(course.changes)
    for change in changes:
        print(change)


@bacli.command
def overview(all: bool = False, fullnames: bool = False):
    program.course.FULL_NAMES = fullnames

    current(fullnames=fullnames)
    solution(fullnames=fullnames)
    legend()

    mandatory = list()
    electives = list()
    for c in getCourses():
        if c.isElectiveGroup:
            continue
        elif c.isElective:
            electives.append(c)
        else:
            mandatory.append(c)
    courses = mandatory + electives

    changesMap = defaultdict(list)
    for course in getCourses():
        for change in course.changes:
            if "verplaatst" in change:
                changesMap[course].append(change)
            if "naar {}".format(course.shortName) in change:
                changesMap[course].append(change)
            elif "studiepunten van {}".format(course.shortName) in change:
                changesMap[course].append(change)

    template = env.get_template('overview.tex')
    output = getOutputPath("overview.tex")
    renderTemplate(template, output, courses=courses, changesMap=changesMap)

    if all:
        outputPath = getOutputPath("Overview")
        os.makedirs(outputPath, exist_ok=True)

        for course in tqdm(courses):
            template = env.get_template('normal.dot')
            output = os.path.join(outputPath, "{}_solution_rel.dot".format(course.id))
            renderDot(template, output,
                      title="Voorstel Relatief ({} gehighlight)".format(course.shortName),
                      includeWorkload=True,
                      absolute=False,
                      fullnames=fullnames,
                      highlightCourse=course
                      )


@bacli.command
def simulate(failures: int = 1, solution: bool = False):
    if solution:
        doSolution()

    courses = getCourses()
    electives = [KZVK1, KZVK2]
    electiveCredits = 0
    for elective in electives:
        courses.remove(elective)
        electiveCredits += elective.sp
    s = Simulator(YEARS, courses, electiveCredits)
    s.simulate(nrFailures=failures)


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

    # LA
    LA.addNewDependency(DW)

    # PPD
    PPD.addNewDependency(PSE, soft=True)

    # WP
    WP.getDependency(GP).remove()
    WP.addNewDependency(IP)

    # SE
    SE.getDependency(IDBS).remove()
    SE.getDependency(PPD).remove()
    SE.getDependency(GAS).remove()
    # SE.getDependency(TA).remove()             # Feedback Serge
    SE.addNewDependency(PSE)

    # DS
    # DS.getDependency(GP).remove()
    # DS.addNewDependency(IDBS)                 # to move DS to year 2
    # DS.getDependency(US).remove()               # to move DS to year 2
    # DS.addNewDependency(CSA)                    # to move DS to year 2

    # AI
    AI.getDependency(AC).remove()
    AI.addNewDependency(GAS)

    # DSGA
#    DSGA.addNewDependency(AC, soft=True)       # Benny
    DSGA.addNewDependency(GAS)

    # AC
    # AC.addNewDependency(MB)
    # AC.getDependency(GAS).remove()            # Floris & Studenten (Laurens)
    AC.getDependency(TA).remove()

    # COMP
    # COMP.addNewDependency(GP, soft=True)
    # COMP.addNewDependency(MB, soft=True)
    # COMP.getDependency(CSA).remove()
    # COMP.getDependency(TA).remove()
    # COMP.getDependency(GAS).remove()          # Feedback Serge

    # CB
    CB.getDependency(LA).remove()
    CB.getDependency(CALC).remove()

    # BAE
    BAE.getDependency(GP).setSoft(True)
    BAE.getDependency(PPD).setSoft(True)


def doSolutionCourses():
    pass
    # move courses
    # US.moveTo(year2.semester2)

    # DS.moveTo(year2.semester1)                  # Studenten (Laurens)
    # AI.moveTo(year2.semester1)                  #

    # AC.moveTo(year3.semester2)                  # instead of compilers?
    # COMP.moveTo(year3.semester2)

    # DSGA.moveTo(year3.semester1)


    # FYS.moveTo(KZVK2)
    # DSGA.setSp(6)
    # KZVK2.setSp(6)


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
    renderDot(template, output, includeWorkload=not noWorkload, absolute=True)
    output = getOutputPath("solution3_rel.dot")
    renderDot(template, output, includeWorkload=not noWorkload, absolute=False)


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
