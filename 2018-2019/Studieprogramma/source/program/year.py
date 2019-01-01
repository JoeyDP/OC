from .course_collection import *


class Year(ICourseCollection):
    def __init__(self, nr):
        super().__init__()
        self.nr = nr
        self.semester1 = Semester(1, self)
        self.semester2 = Semester(2, self)

    @property
    def courses(self):
        return self.semester1.courses + self.semester2.courses

    @property
    def semesters(self):
        return [self.semester1, self.semester2]

    @property
    def name(self):
        return "Ba {}".format(self.nr)

    @property
    def id(self):
        return "ba{}".format(self.nr)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.id

    def __lt__(self, other):
        return self.nr < other.nr

    def __le__(self, other):
        return self.nr <= other.nr


class Semester(CourseList):
    def __init__(self, nr, year):
        super().__init__()
        self.nr = nr
        self.year = year

    @property
    def id(self):
        return "sem{}".format(self.nr)

    def __str__(self):
        return "{} semester {}".format(str(self.year), self.nr)

    def __repr__(self):
        return self.year.id + self.id

    def __lt__(self, other):
        return self.year < other.year or self.nr < other.nr

    def __le__(self, other):
        return self.year < other.year or (self.year == other.year and self.nr <= other.nr)


year1 = Year(1)
year2 = Year(2)
year3 = Year(3)
