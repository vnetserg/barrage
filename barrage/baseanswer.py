
from .attributed import Attributed

class BaseAnswer(Attributed):
    @classmethod
    def from_stdout(cls, stdout):
        raise NotImplementedError

    @classmethod
    def for_problem(cls, problem):
        raise NotImplementedError

    def validate(self, prob):
        return self.for_problem(prob) == self

    def to_stdout(self):
        return str(self)
