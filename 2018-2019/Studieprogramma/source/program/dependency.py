from functools import lru_cache


from .status import Status


@lru_cache(maxsize=None)
class Dependency(object):
    """ Dependency for course """
    def __init__(self, source, dest, soft=False, new=False, together=False):
        self.source = source
        self.dest = dest
        self.soft = soft
        self.together = together
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
        return self.soft or self.together

    def setSoft(self, b):
        if self.soft == b:
            raise RuntimeError("setSoft to same value as before.")
        self.status = Status.Changed
        self.soft = b
        change = "Dependency van {} naar {} verzwakt.".format(self.source.shortName, self.dest.shortName)
        self.source.logChange(change)
        self.dest.logChange(change)

    def validate(self):
        if self.status == Status.Removed:
            return

        if self.together:
            # Should occur in same year
            assert self.source.year == self.dest.year
        elif self.isSoft():
            # Should occur before, but can be in same semester
            assert self.source.semester <= self.dest.semester, "{} should be before {}".format(self.source, self.dest)
        else:
            # Should be before
            assert self.source.semester < self.dest.semester, "{} should be before {}".format(self.source, self.dest)


