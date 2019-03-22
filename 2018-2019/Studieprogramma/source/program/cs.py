
from .year import *
from .course import Course, ElectiveGroup
from .teacher import Teacher


# ===================
# =     Teachers    =
# ===================

HANS = Teacher("Hans", "Vangheluwe")
ELS = Teacher("Els", "Laenens")
BART = Teacher("Bart", "Goethals")
TOON = Teacher("Toon", "Calders")
KRIS = Teacher("Kris", "Laukens")
BENNY = Teacher("Benny", "Van Houdt")
STIJN_S = Teacher("Stijn", "Symens")
SERGE = Teacher("Serge", "Demeyer")
FLORIS = Teacher("Floris", "Geerts")
WERNER_PEETERS = Teacher("Werner", "Peeters")
JOKE_H = Teacher("Joke", "Haderman")
JAN_B = Teacher("Jan", "Broeckhove")
LIEVEN_LE_BRUYN = Teacher("Lieven", "Le Bruyn")
KAREL_INT_HOUT = Teacher("Karel", "In't Hout")
GUILLERMO_ALBERTO_PEREZ = Teacher("Guillermo Alberto", "Perez")
STEVEN_L = Teacher("Steven", "Latré")
PATRICK_L = Teacher("Patrick", "Loobuyck")
CHRIS_B = Teacher("Chris", "Blondia")
ANNIE_C = Teacher("Annie", "Cuyt")
JAN_BOUCKAERT = Teacher("Jan", "Bouckaert")

NNB = Teacher("", "NNB")


# ==================
# =     Courses    =
# ==================

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
NA = Course("Numerieke Analyse", "NA", 3, year2.semester2, KAREL_INT_HOUT, spWork=0)
ES = Course("Elementaire Statistiek", "ES", 3, year2.semester2, NNB, spWork=1)
COMP = Course("Compilers", "COMP", 6, year2.semester2, GUILLERMO_ALBERTO_PEREZ, spWork=3)

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
DSGA = Course("Datastructuren en Graafalgoritmen", "DSGA", 3, year3.semester2, BENNY, spWork=0)
LBS = Course("Levensbeschouwing", "LBS", 3, year3.semester2, PATRICK_L, spWork=0)
FYS = Course("Fysica", "FYS", 6, year3.semester2, JOKE_H, spWork=0)
BAE = Course("Bachelor Eindwerk", "BAE", 12, year3.semester2, JAN_B, spWork=12)


KZVK2 = ElectiveGroup("Keuzevakken 2", "KZVK2", 3, year3.semester2)
CB = Course("Inleiding tot Computationele Biologie", "CB", 3, KZVK2, KRIS, spWork=2)
INDP = Course("Individueel Project", "INDP", 6, KZVK2, ELS, spWork=6)
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