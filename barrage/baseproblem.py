
from .attributed import Attributed
from .baseanswer import BaseAnswer

class BaseProblem(Attributed):
    def __init__(self, *args, **kw):
        if isinstance(args[-1], BaseAnswer):
            self.answer = args[-1]
            args = args[:-1]
        else:
            self.answer = None
        self.check_answer = kw.pop("check_answer", True)
        self.sanitize = kw.pop("sanitize", True)
        super().__init__(*args, **kw)
        if self.answer and not self.answer.validate(self):
            raise ValueError("invalid answer given in the constructor. {}, {}".format(self, self.answer))

    def to_stdin(self):
        raise NotImplemented
