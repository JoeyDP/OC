import itertools

from .year import *
from .teacher import *
from .dependency import Dependency
from .status import Status

BASE_HEIGHT = 0.25
PADDING = 0.2
FULL_NAMES = False


class Course(object):
    def __init__(self, name, shortName, sp, semester, teacher, spWork=0):
        assert spWork <= sp
        self.name = name
        self._shortName = shortName
        self.teacher = teacher
        if teacher:
            teacher.addCourse(self)
        self.sp = sp
        self.spWork = spWork
        self.semester = semester
        semester.addCourse(self)
        self.dependsOn = dict()
        self.requiredFor = dict()
        self.status = Status.Normal
        self.changes = list()

    @property
    def shortName(self):
        if FULL_NAMES:
            return self.name
        else:
            return self._shortName

    @property
    def id(self):
        to_underscore = [' ', ':', ',']
        stripped = self._shortName.replace('&', '')
        for char in to_underscore:
            stripped = stripped.replace(char, '_')
        return stripped

    @property
    def year(self):
        return self.semester.year

    @property
    def spTheory(self):
        return self.sp - self.spWork

    @property
    def height(self):
        h = (BASE_HEIGHT + PADDING) * (self.sp / 3) - PADDING
        return max(h, 0.2)

    @property
    def isElectiveGroup(self):
        return False

    @property
    def isElective(self):
        return isinstance(self.semester, ElectiveGroup)

    def logChange(self, change: str):
        self.changes.append(change)

    def addDependency(self, course, soft=False, new=False, together=False):
        d = self.dependsOn[course] = Dependency(course, self, soft=soft, new=new, together=together)
        course.requiredFor[self] = d
        return d

    def addNewDependency(self, course, soft=False):
        change = "Nieuwe dependency toegevoegd van {} naar {}.".format(course.shortName, self.shortName)
        self.logChange(change)
        course.logChange(change)
        return self.addDependency(course, soft=soft, new=True)

    def getDependency(self, course):
        return self.dependsOn[course]

    def getDependencies(self):
        values = self.dependsOn.values()
        return values

    def getDependants(self):
        return self.requiredFor.values()

    def validate(self):
        for dep in self.dependsOn.values():
            dep.validate()

    def moveTo(self, semester):
        if semester == self.semester:
            raise RuntimeError("Tried to move course to same semester")
        self.logChange("Vak {} van {} naar {} verplaatst.".format(self.shortName, self.semester, semester))
        self.semester.removeCourse(self)
        self.semester = semester
        self.semester.addCourse(self)
        self.status = Status.Changed

    def setSp(self, sp):
        if self.sp == sp:
            raise RuntimeError("Tried to set SP to same amount")

        if self.sp < sp:
            self.status = Status.New            # green for added SP
            self.logChange("Aantal studiepunten van {} verhoogd van {} naar {}.".format(self.shortName, self.sp, sp))
        else:
            self.status = Status.Reduced        # green for removed SP
            self.logChange("Aantal studiepunten van {} verminderd van {} naar {}.".format(self.shortName, self.sp, sp))
        self.sp = sp

    def remove(self):
        self.status = Status.Removed

    def hasChanges(self):
        """ Is part of any change (both course and its dependencies). """
        return len(self.changes) != 0

    @property
    def changed(self):
        """ Is the course itself changed. """
        return self.status == Status.Changed

    @property
    def new(self):
        return self.status == Status.New

    @property
    def removed(self):
        return self.status == Status.Removed

    @property
    def reduced(self):
        return self.status == Status.Reduced

    def __str__(self):
        return self.name

    def __repr__(self):
        return self._shortName

    def __lt__(self, other):
        return self.semester < other.semester

    def __le__(self, other):
        return self.semester <= other.semester


class ElectiveGroup(Course):
    def __init__(self, name, shortName, sp, semester):
        super().__init__(name, shortName, sp, semester, None, spWork=0)
        self._courses = list()

    @property
    def courses(self):
        return self._courses

    @property
    def isElectiveGroup(self):
        return True

    def addCourse(self, course):
        self.courses.append(course)
        self.semester.addCourse(course)

    def removeCourse(self, course):
        self.courses.remove(course)
        self.semester.removeCourse(course)


def createCluster(courses):
    for course1, course2 in itertools.combinations(courses, 2):
        course1.addDependency(course2, together=True)
        # course2.addDependency(course1, together=True)

