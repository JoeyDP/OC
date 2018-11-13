
from year import *


BASE_HEIGHT = 0.25
PADDING = 0.2


class Course(object):
    def __init__(self, name, shortName, sp, semester, spWork=0):
        assert spWork <= sp
        self.name = name
        self.shortName = shortName
        self.sp = sp
        self.spWork = spWork
        self.semester = semester
        semester.addCourse(self)

    @property
    def id(self):
        return self.shortName.replace('&', '')

    @property
    def spTheory(self):
        return self.sp - self.spWork

    @property
    def height(self):
        return (BASE_HEIGHT + PADDING) * (self.sp / 3) - PADDING

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.shortName


# Year 1
# Semester 1
IP = Course("Inleiding Programmeren", "IP", 9, year1.semester1, spWork=5)
DW = Course("Discrete Wiskunde", "DW", 9, year1.semester1, spWork=0)
CSA = Course("Computersystemen en -architectuur", "CSA", 9, year1.semester1, spWork=4)
GAS = Course("Gegevensabstractie en -structuren", "GAS", 6, year1.semester1, spWork=3)

# Semester 2
TA = Course("Talen en Automaten", "T&A", 6, year1.semester2, spWork=3)
PSE = Course("Project Software Engineering", "PSE", 6, year1.semester2, spWork=6)
CALC = Course("Calculus", "CALC", 9, year1.semester2, spWork=0)
CG = Course("Computer Graphics", "CG", 6, year1.semester2, spWork=3)


# Year2
# Semester 1
GP = Course("Gevorderd Programmeren", "GP", 6, year2.semester1, spWork=2)
MB = Course("Machines en Berekenbaarheid", "M&B", 6, year2.semester1, spWork=3)
US = Course("Uitbatingssystemen", "US", 6, year2.semester1, spWork=0)
IDBS = Course("Introduction to Databases", "IDBS", 6, year2.semester1, spWork=0)
LA = Course("Lineaire Algebra", "LA", 6, year2.semester1, spWork=0)

# Semester 2
AC = Course("Algoritmen en Complexiteit", "A&C", 6, year2.semester2, spWork=0)
PPD = Course("Programming Project Databases", "PPD", 6, year2.semester2, spWork=6)
CN = Course("Computernetwerken", "CN", 6, year2.semester2, spWork=0)
FYS = Course("Fysica", "FYS", 6, year2.semester2, spWork=0)
NA = Course("Numerieke Analyse", "NA", 3, year2.semester2, spWork=0)
ES = Course("Elementaire Statistiek", "ES", 3, year2.semester2, spWork=1)


# Year3
# Semester 1
WP = Course("Wetenschappelijk Programmeren", "WP", 6, year3.semester1, spWork=3)
SE = Course("Software Engineering", "SE", 6, year3.semester1, spWork=3)
TCS = Course("Telecommunicatiesystemen", "TCS", 6, year3.semester1, spWork=3)
DS = Course("Gedistribueerde Systemen", "DS", 6, year3.semester1, spWork=3)
AI = Course("Aritifical Intelligence", "AI", 6, year3.semester1, spWork=3)

# Semester 2
DSGA = Course("Datastructuren en Graafalgoritmen", "DSGA", 3, year3.semester2, spWork=0)
COMP = Course("Compilers", "COMP", 6, year3.semester2, spWork=3)
LBS = Course("Levensbeschouwing", "LBS", 3, year3.semester2, spWork=0)
BAE = Course("Bachelor Eindwerk", "BAE", 12, year3.semester2, spWork=12)
KZVK = Course("Keuzevakken", "KZVK", 6, year3.semester2, spWork=0)

