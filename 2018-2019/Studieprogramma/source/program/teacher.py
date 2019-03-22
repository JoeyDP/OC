from .course_collection import CourseList


class Teacher(CourseList):
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

    def __repr__(self):
        return self.fullName

