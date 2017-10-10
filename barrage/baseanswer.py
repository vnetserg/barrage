
from .attributed import Attributed

class BaseAnswer(Attributed):
    @classmethod
    def from_stdout(cls, stdout):
        raise NotImplemented

    @classmethod
    def for_problem(cls, problem):
        raise NotImplemented

    def validate(self, prob):
        return self.for_problem(prob) == self

    def to_stdout(self):
        return str(self)
