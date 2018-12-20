

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
