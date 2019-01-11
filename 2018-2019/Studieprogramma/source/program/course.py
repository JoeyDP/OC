
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
        return self._shortName.replace('&', '')

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

    def addDependency(self, course, soft=False, new=False):
        d = self.dependsOn[course] = Dependency(course, self, soft=soft, new=new)
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


# Year 1
# Semester 1
IP = Course("Inleiding Programmeren", "IP", 9, year1.semester1, TOON, spWork=5)
DW = Course("Discrete Wiskunde", "DW", 9, year1.semester1, STIJN_S, spWork=0)
CSA = Course("Computersystemen en -architectuur", "CSA", 9, year1.semester1, HANS, spWork=4)
GAS = Course("Gegevensabstractie en -structuren", "GAS", 6, year1.semester1, ELS, spWork=3)

# Semester 2
TA = Course("Talen en Automaten", "T&A", 6, year1.semester2, ELS, spWork=3)
PSE = Course("Project Software Engineering", "PSE", 6, year1.semester2, SERGE, spWork=6)
CALC = Course("Calculus", "CALC", 9, year1.semester2, WERNER_PEETERS, spWork=0)
CG = Course("Computer Graphics", "CG", 6, year1.semester2, BENNY, spWork=3)


# Year2
# Semester 1
GP = Course("Gevorderd Programmeren", "GP", 6, year2.semester1, JAN_B, spWork=2)
MB = Course("Machines en Berekenbaarheid", "M&B", 6, year2.semester1, ELS, spWork=3)
US = Course("Uitbatingssystemen", "US", 6, year2.semester1, BENNY, spWork=0)
IDBS = Course("Introduction to Databases", "IDBS", 6, year2.semester1, TOON, spWork=0)
LA = Course("Lineaire Algebra", "LA", 6, year2.semester1, LIEVEN_LE_BRUYN, spWork=0)

# Semester 2
AC = Course("Algoritmen en Complexiteit", "A&C", 6, year2.semester2, FLORIS, spWork=0)
PPD = Course("Programming Project Databases", "PPD", 6, year2.semester2, BART, spWork=6)
CN = Course("Computernetwerken", "CN", 6, year2.semester2, CHRIS_B, spWork=0)
FYS = Course("Fysica", "FYS", 6, year2.semester2, JOKE_H, spWork=0)
NA = Course("Numerieke Analyse", "NA", 3, year2.semester2, KAREL_INT_HOUT, spWork=0)
ES = Course("Elementaire Statistiek", "ES", 3, year2.semester2, NNB, spWork=1)


# Year3
# Semester 1
WP = Course("Wetenschappelijk Programmeren", "WP", 6, year3.semester1, ANNIE_C, spWork=3)
SE = Course("Software Engineering", "SE", 6, year3.semester1, SERGE, spWork=3)
TCS = Course("Telecommunicatiesystemen", "TCS", 6, year3.semester1, CHRIS_B, spWork=3)
DS = Course("Gedistribueerde Systemen", "DS", 6, year3.semester1, STEVEN_L, spWork=3)
AI = Course("Aritifical Intelligence", "AI", 6, year3.semester1, BART, spWork=3)
KZVK1 = ElectiveGroup("Keuzevakken 1", "KZVK1", 3, year3.semester1)
ECON = Course("Economie", "ECON", 3, KZVK1, JAN_BOUCKAERT, spWork=0)
CT = Course("Codetheorie", "CT", 3, KZVK1, STIJN_S, spWork=2)

# Semester 2
COMP = Course("Compilers", "COMP", 6, year3.semester2, GUILLERMO_ALBERTO_PEREZ, spWork=3)
DSGA = Course("Datastructuren en Graafalgoritmen", "DSGA", 3, year3.semester2, BENNY, spWork=0)
LBS = Course("Levensbeschouwing", "LBS", 3, year3.semester2, PATRICK_L, spWork=0)
BAE = Course("Bachelor Eindwerk", "BAE", 12, year3.semester2, JAN_B, spWork=12)

KZVK2 = ElectiveGroup("Keuzevakken 2", "KZVK2", 3, year3.semester2)
CB = Course("Inleiding tot Computationele Biologie", "CB", 3, KZVK2, KRIS, spWork=2)
INDP = Course("Individueel Project", "INDP", 6, KZVK2, ELS, spWork=3)
TL = Course("Toegepaste Logica", "TL", 3, KZVK2, ELS, spWork=3)
LCN = Course("Labo Computernetwerken", "LCN", 3, KZVK2, CHRIS_B, spWork=3)


# =======================
# =     Dependencies    =
# =======================

# GP
GP.addDependency(IP)
GP.addDependency(CG)
GP.addDependency(PSE)
GP.addDependency(CSA)

# M&B
MB.addDependency(TA)

# US
US.addDependency(CSA)

# IDBS
IDBS.addDependency(GAS)

# LA
# /

# A&C
AC.addDependency(DW)
AC.addDependency(TA)
AC.addDependency(GAS)

# PPD
PPD.addDependency(IDBS, soft=True)

# CN
CN.addDependency(DW)
CN.addDependency(CSA)
CN.addDependency(CALC)

# FYS
# /

# NA
# /

# ES
# /

# =====================
# =	dependencies 3Ba	=
# =====================

# WP
WP.addDependency(CALC)
WP.addDependency(GP)
WP.addDependency(LA)
WP.addDependency(NA)

# SE
SE.addDependency(TA)
SE.addDependency(GAS)
SE.addDependency(IDBS, soft=True)
SE.addDependency(PPD, soft=True)

# TCS
TCS.addDependency(GP)
TCS.addDependency(CN)

# DS
DS.addDependency(GP)
DS.addDependency(US)

# AI
AI.addDependency(AC)

# DSGA
# /

# COMP
COMP.addDependency(CSA)
COMP.addDependency(TA)
COMP.addDependency(GAS)

# LBS
# /

# BAE
BAE.addDependency(GP)
BAE.addDependency(PPD)

BAE.addDependency(SE, soft=True)
BAE.addDependency(TCS, soft=True)
BAE.addDependency(DS, soft=True)
BAE.addDependency(AI, soft=True)
BAE.addDependency(COMP, soft=True)

# CT
CT.addDependency(LA, soft=True)

# ECON
# /

# INDP
# /

# CB
CB.addDependency(IP)
CB.addDependency(DW)
CB.addDependency(CALC)
CB.addDependency(LA)

# LCN
LCN.addDependency(CN)

# TL
TL.addDependency(MB)
