from functools import lru_cache

from enum import Enum


class Status(Enum):
    Normal = 0
    New = 1
    Changed = 2
    Removed = 3


@lru_cache(maxsize=None)
class Dependency(object):
    """ Dependency for course """
    def __init__(self, source, dest, soft=False, new=False):
        self.source = source
        self.dest = dest
        self.soft = soft
        self.status = Status.New if new else Status.Normal
        self.validate()

    def remove(self):
        self.status = Status.Removed
        change = "Dependency van {} naar {} verwijderd.".format(self.source.shortName, self.dest.shortName)
        self.source.logChange(change)
        self.dest.logChange(change)

    def isNew(self):
        return self.status == Status.New

    def isChanged(self):
        return self.status == Status.Changed

    def isRemoved(self):
        return self.status == Status.Removed

    def isSoft(self):
        return self.soft

    def setSoft(self, b):
        if self.soft == b:
            raise RuntimeError("setSoft to same value as before.")
        self.status = Status.Changed
        self.soft = b
        change = "Dependency van {} naar {} verzwakt.".format(self.source.shortName, self.dest.shortName)
        self.source.logChange(change)
        self.dest.logChange(change)

    def validate(self):
        if self.status != Status.Removed:
            if self.isSoft():
                assert self.source.semester <= self.dest.semester, "{} should be before {}".format(self.source, self.dest)
            else:
                assert self.source.year < self.dest.year, "{} should be before {}".format(self.source, self.dest)


