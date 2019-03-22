
from .year import *
from .course import Course, ElectiveGroup, createCluster
from .teacher import Teacher


# ===================
# =     Teachers    =
# ===================

# find:     (.*);(.*);(.*)
# replace:  $1 = Teacher("$3", "$2")
HANS = Teacher("Hans", "Vangheluwe")

BERTELS_INGE = Teacher("Inge", "Bertels")
VERWULGEN_STIJN = Teacher("Stijn", "Verwulgen")
BARBIER_HANS = Teacher("Hans", "Barbier")
BELMANS_BERT = Teacher("Bert", "Belmans")
DE_VOS_ELS = Teacher("Els", "De Vos")
PASSCHYN_RENAAT = Teacher("Renaat", "Passchyn")
VAN_DE_VREKEN_KOEN = Teacher("Koen", "Van de vreken")
CORNELIS_GUSTAAF = Teacher("Gustaaf", "Cornelis")
THOMAES_JAN = Teacher("Jan", "Thomaes")
GELDOF_DIRK = Teacher("Dirk", "Geldof")
DRIESEN_GEERT = Teacher("Geert", "Driesen")
VAN_ROMPAEY_JOHAN = Teacher("Johan", "Van Rompaey")
JANSEN_WIM = Teacher("Wim", "Jansen")
MYS_CHRISTIAAN = Teacher("Christiaan", "Mys")
SCHRIJVER_LARA = Teacher("Lara", "Schrijver")
VALLET_NATHALIE = Teacher("Nathalie", "Vallet")
VERBRUGGEN_SVEN = Teacher("Sven", "Verbruggen")
LOOBUYCK_PATRICK = Teacher("Patrick", "Loobuyck")

NNB = Teacher("", "NNB")


# ==================
# =     Courses    =
# ==================

# find:     (.*);(.*);(.*);(.*);(.*)
# replace:  $1 = Course("$2", "$2", $3, year1.semester$4, $5)

# Year 1
# Semester 1
ARCH_1042FOWARC = Course("Architectuurgesch. en de cultuur van ...", "Architectuurgeschiedenis", 6, year1.semester1, BERTELS_INGE)
ARCH_1031FOWARC = Course("Meetkunde voor ontwerpers", "Meetkunde voor ontwerpers", 3, year1.semester1, VERWULGEN_STIJN)
ARCH_1003FOWARC = Course("Initiatie ontwerp", "Initiatie ontwerp", 12, year1.semester1, BARBIER_HANS)
ARCH_1046FOWARC = Course("Statica", "Statica", 3, year1.semester1, PASSCHYN_RENAAT)
ARCH_1048FOWARC = Course("Initiatie materiaalleer", "Initiatie materiaalleer", 3, year1.semester1, BELMANS_BERT)
ARCH_1049FOWARC = Course("Initiatie bouwfysica", "Initiatie bouwfysica", 3, year1.semester1, PASSCHYN_RENAAT)

# Semester 2
ARCH_1043FOWARC = Course("Structuuranalyse", "Structuuranalyse", 3, year1.semester2, BELMANS_BERT)
ARCH_1044FOWARC = Course("Wooncultuur", "Wooncultuur", 3, year1.semester2, DE_VOS_ELS)
ARCH_1038FOWARC = Course("Initiatie ontwerp: casus", "Initiatie ontwerp: casus", 3, year1.semester2, BARBIER_HANS)
ARCH_1045FOWARC = Course("Studiereis 1", "Studiereis 1", 3, year1.semester2, BERTELS_INGE)
ARCH_1041FOWARC = Course("Initiatie ontw: architectonisch ontw", "Initiatie ontwerp: architectonisch ontwerp", 9, year1.semester2, BARBIER_HANS)
ARCH_1047FOWARC = Course("Sterkteleer", "Sterkteleer", 3, year1.semester2, PASSCHYN_RENAAT)
ARCH_1050FOWARC = Course("Constructie 1", "Constructie 1", 3, year1.semester2, VAN_DE_VREKEN_KOEN)
ARCH_1051FOWARC = Course("Materiaalleer", "Materiaalleer", 3, year1.semester2, BELMANS_BERT)


# Year2
# Semester 1
ARCH_1052FOWARC = Course("Arch. en cultuur: filosofie", "Architectuur en cultuur: filosofie", 3, year2.semester1, CORNELIS_GUSTAAF)
ARCH_1053FOWARC = Course("Arch. en cultuur: geschiedenis", "Architectuur en cultuur: geschiedenis", 3, year2.semester1, BERTELS_INGE)
ARCH_1064FOWARC = Course("Arch. en cultuur: casus", "Architectuur en cultuur: casus", 6, year2.semester1, THOMAES_JAN)
ARCH_1011FOWARC = Course("Arch. en cultuur: architectonisch ontw", "Architectuur en cultuur: architectonisch ontwerp", 9, year2.semester1, THOMAES_JAN)
ARCH_1058FOWARC = Course("Constructie 2", "Constructie 2", 6, year2.semester1, VAN_DE_VREKEN_KOEN)
ARCH_1059FOWARC = Course("Bouwfysica", "Bouwfysica", 3, year2.semester1, VAN_ROMPAEY_JOHAN)

# Semester 2
ARCH_1066FOWARC = Course("Arch. en omg.: landsch, stad en ... ", "Architectuur en omgeving: landschap, stad en openbare ruimte", 6, year2.semester2, BERTELS_INGE)
ARCH_1056FOWARC = Course("Arch. en omg.: sociologie en de stad", "Architectuur en omgeving: sociologie en de stad", 3, year2.semester2, GELDOF_DIRK)
ARCH_1035FOWARC = Course("Arch. en omg.: casus", "Architectuur en omgeving: casus", 3, year2.semester2, DRIESEN_GEERT)
ARCH_1057FOWARC = Course("Studiereis 2", "Studiereis 2", 3, year2.semester2, BERTELS_INGE)
ARCH_1014FOWARC = Course("Arch. en omg.: architectonisch ontw", "Architectuur en omgeving: architectonisch ontwerp", 9, year2.semester2, DRIESEN_GEERT)
ARCH_1015FOWARC = Course("Simulatie van structuurelementen", "Simulatie van structuurelementen", 6, year2.semester2, PASSCHYN_RENAAT)


# Year3
# Semester 1
ARCH_1060FOWARC = Course("Arch. en const.: bouwknopen", "Architectuur en constructie: bouwknopen", 3, year3.semester1, VAN_ROMPAEY_JOHAN)
ARCH_1061FOWARC = Course("Arch. en const.: bouwsystemen", "Architectuur en constructie: bouwsystemen", 3, year3.semester1, JANSEN_WIM)
ARCH_1065FOWARC = Course("Arch. en const.: casus", "Architectuur en constructie: casus", 6, year3.semester1, MYS_CHRISTIAAN)
ARCH_1019FOWARC = Course("Arch. en const.: architectonisch ontw", "Architectuur en constructie: architectonisch ontwerp", 9, year3.semester1, MYS_CHRISTIAAN)
ARCH_1020FOWARC = Course("Architectuurtheorie", "Architectuurtheorie", 6, year3.semester1, SCHRIJVER_LARA)
ARCH_1001FOWLVB = Course("Levensbeschouwing en publieke ruimte", "Levensbeschouwing en publieke ruimte", 3, year3.semester1, LOOBUYCK_PATRICK)

# Semester 2
ARCH_1021FOWARC = Course("Schrijven over architectuur", "Schrijven over architectuur", 6, year3.semester2, VALLET_NATHALIE)
ARCH_1062FOWARC = Course("Studiereis 3", "Studiereis 3", 3, year3.semester2, BERTELS_INGE)
ARCH_1039FOWARC = Course("Architectonisch ontwerp: 1:1", "Architectonisch ontwerp: 1:1", 9, year3.semester2, VAN_ROMPAEY_JOHAN)
ARCH_1023FOWARC = Course("Bachelorproef", "Bachelorproef", 12, year3.semester2, VERBRUGGEN_SVEN)



# =======================
# =     Dependencies    =
# =======================

# Year 1

# Initiatie ontwerp: casus
# Initiatie ontwerp: architectonisch ontwerp
createCluster([ARCH_1041FOWARC, ARCH_1038FOWARC])


# Year 2

# Architectuur en cultuur: filosofie
# Architectuur en cultuur: geschiedenis
# Architectuur en cultuur: casus
# Architectuur en cultuur: architectonisch ontwerp
createCluster([ARCH_1052FOWARC, ARCH_1053FOWARC, ARCH_1011FOWARC, ARCH_1064FOWARC])

# Architectuur en cultuur: architectonisch ontwerp
ARCH_1011FOWARC.addDependency(ARCH_1003FOWARC)
ARCH_1011FOWARC.addDependency(ARCH_1041FOWARC)

# Architectuur en omgeving: landschap, stad en openbare ruimte
# Architectuur en omgeving: sociologie en de stad
# Architectuur en omgeving: casus
# Architectuur en omgeving: architectonisch ontwerp
createCluster([ARCH_1066FOWARC, ARCH_1056FOWARC, ARCH_1035FOWARC, ARCH_1014FOWARC])

# Architectuur en omgeving: architectonisch ontwerp
ARCH_1014FOWARC.addDependency(ARCH_1003FOWARC)
ARCH_1014FOWARC.addDependency(ARCH_1041FOWARC)

# Constructie 2
ARCH_1058FOWARC.addDependency(ARCH_1050FOWARC)

# Year 3

# Architectuur en constructie: bouwknopen
# Architectuur en constructie: bouwsystemen
# Architectuur en constructie: casus
# Architectuur en constructie: architectonisch ontwerp
createCluster([ARCH_1060FOWARC, ARCH_1061FOWARC, ARCH_1065FOWARC, ARCH_1019FOWARC])

# Architectuur en constructie: architectonisch ontwerp
ARCH_1019FOWARC.addDependency(ARCH_1003FOWARC)
ARCH_1019FOWARC.addDependency(ARCH_1041FOWARC)
ARCH_1019FOWARC.addDependency(ARCH_1011FOWARC)
ARCH_1019FOWARC.addDependency(ARCH_1014FOWARC)

# Architectonisch ontwerp: 1:1
ARCH_1039FOWARC.addDependency(ARCH_1011FOWARC)
ARCH_1039FOWARC.addDependency(ARCH_1014FOWARC)
ARCH_1039FOWARC.addDependency(ARCH_1019FOWARC, soft=True)

# Bachelorproef
ARCH_1023FOWARC.addDependency(ARCH_1011FOWARC)
ARCH_1023FOWARC.addDependency(ARCH_1014FOWARC)
ARCH_1023FOWARC.addDependency(ARCH_1019FOWARC, soft=True)
