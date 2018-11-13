

class CourseCollection(object):
    @property
    def courses(self):
        raise NotImplementedError

    @property
    def spTotal(self):
        return sum(course.sp for course in self.courses)

    @property
    def spWork(self):
        return sum(course.spWork for course in self.courses)

    @property
    def spTheory(self):
        return sum(course.spTheory for course in self.courses)


class Year(CourseCollection):
    def __init__(self, nr):
        self.nr = nr
        self.semester1 = Semester(1)
        self.semester2 = Semester(2)

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


class Semester(CourseCollection):
    def __init__(self, nr):
        self.nr = nr
        self._courses = list()

    @property
    def courses(self):
        return self._courses

    def addCourse(self, course):
        self.courses.append(course)

    def removeCourse(self, course):
        self.courses.remove(course)

    @property
    def id(self):
        return "sem{}".format(self.nr)


year1 = Year(1)
year2 = Year(2)
year3 = Year(3)