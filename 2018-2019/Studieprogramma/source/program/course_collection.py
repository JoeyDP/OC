

class ICourseCollection(object):
    @property
    def courses(self):
        raise NotImplementedError

    @property
    def spTotal(self):
        return sum(course.sp for course in self.courses if not course.isElective)

    @property
    def spWork(self):
        return sum(course.spWork for course in self.courses if not course.isElective)

    @property
    def spTheory(self):
        return sum(course.spTheory for course in self.courses if not course.isElective)

    @property
    def spTotalAll(self):
        return sum(course.sp for course in self.courses)

    @property
    def spWorkAll(self):
        return sum(course.spWork for course in self.courses)

    @property
    def spTheoryAll(self):
        return sum(course.spTheory for course in self.courses)


class CourseCollection(ICourseCollection):
    def __init__(self, items=None):
        super().__init__()
        if items:
            self._courses = list(items)
        else:
            self._courses = list()

    @property
    def courses(self):
        return self._courses

    def __contains__(self, item):
        return item in self.courses

    def __iter__(self):
        return iter(self.courses)

    def __len__(self):
        return len(self.courses)

    def __str__(self):
        return str(self.courses)

    def __repr__(self):
        return repr(self.courses)

    def addCourse(self, course):
        self.courses.append(course)

    def removeCourse(self, course):
        self.courses.remove(course)
