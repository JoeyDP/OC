from .course_collection import CourseCollection


class Teacher(CourseCollection):
    all = list()

    def __init__(self, firstName, lastName):
        super().__init__()
        self.firstName = firstName
        self.lastName = lastName
        Teacher.all.append(self)

    @property
    def email(self):
        def clean(s):
            return s.replace(' ', '').replace('\'', '').replace('é', 'e').lower()
        return "{}.{}@uantwerpen.be".format(clean(self.firstName), clean(self.lastName))

    @property
    def name(self):
        return self.fullName

    @property
    def fullName(self):
        return "{} {}".format(self.firstName, self.lastName)

    def __str__(self):
        return self.fullName


# Teachers
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