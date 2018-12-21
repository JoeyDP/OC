import itertools

from .year import *
from .course import *
from .course_collection import CourseCollection


def dependenciesMet(course, credits):
    return all([dependencyMet(dep, credits) for dep in course.getDependencies()])


def dependencyMet(dep, credits):
    if dep.isRemoved():
        return True
    if dep.isSoft():
        # previous ones should always be favored so this is always true for our simulator.
        return True
    else:
        return dep.source in credits


class Simulator(object):
    def __init__(self, years, courses, electiveCredits):
        self.years = years
        self.courses = courses
        self.electiveCredits = electiveCredits

    def simulate(self, nrFailures=1):
        requiredCourses = [c for c in self.courses if not c.isElective]
        scenarios = itertools.combinations_with_replacement(requiredCourses, nrFailures)

        badSet = list()
        for scenario in scenarios:
            toFailset = list(scenario)
            credits = CourseCollection()
            electives = CourseCollection()
            yearNr = 1
            spDistribution = list()
            creditsDistribution = list()
            while credits.spTotalAll < 180:
                # print("Year {}".format(str(yearNr)))
                # print("Done", credits)
                # print("Credits", credits.spTotalAll)
                myCourses = CourseCollection()
                for course in self.courses:
                    # print(course)
                    if course in credits:
                        # print("already done")
                        continue
                    if myCourses.spTotalAll + course.sp > 60:
                        # print("No space")
                        continue
                    if credits.spTotalAll + course.sp > 180:
                        # print("Already did too much courses")
                        continue
                    if course.isElective and electives.spTotalAll + course.sp > self.electiveCredits:
                        # print("Can't take more electives")
                        continue
                    if not dependenciesMet(course, credits):
                        # print("Dep unmet")
                        continue

                    myCourses.addCourse(course)
                    if course.isElective:
                        electives.addCourse(course)


                # print("Taking up courses:", myCourses)
                # print("SP this year:", myCourses.spTotalAll)
                spDistribution.append(myCourses.spTotalAll)
                for toFail in toFailset[:]:
                    if toFail in myCourses:
                        print("Failing", toFail)
                        myCourses.removeCourse(toFail)
                        if toFail.isElective:
                            electives.removeCourse(toFail)      # if it is an elective
                        toFailset.remove(toFail)

                creditsDistribution.append(myCourses.spTotalAll)

                for course in myCourses:
                    credits.addCourse(course)

                yearNr += 1

            print(spDistribution)
            print(creditsDistribution)
            totalCredits = 0
            for sp, c in zip(spDistribution, creditsDistribution):
                totalCredits += c
                if sp <= 36 and totalCredits < 150:
                    print("\t\t !! Nearly underfilled bachelor and cannot start master !!")
                    badSet.append(scenario)

        print("Bottlenecks:")
        for scenario in badSet:
            print("\t", scenario)
