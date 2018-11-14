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
        assert source <= dest, "{} should be before {}".format(source, dest)
        self.source = source
        self.dest = dest
        self.soft = soft
        self.status = Status.New if new else Status.Normal

    def remove(self):
        self.status = Status.Removed

    def isNew(self):
        return self.status == Status.New

    def isChanged(self):
        return self.status == Status.Changed

    def isRemoved(self):
        return self.status == Status.Removed

    def isSoft(self):
        return self.soft

    def setSoft(self, b):
        if self.soft != b:
            self.status = Status.Changed
        self.soft = b

