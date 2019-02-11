
from .attributed import Attributed
from .baseanswer import BaseAnswer

class BaseProblem(Attributed):
    def __init__(self, *args, **kw):
        if isinstance(args[-1], BaseAnswer):
            self.answer = args[-1]
            args = args[:-1]
        else:
            self.answer = kw.pop("answer", None)
        self.check_answer = kw.pop("check_answer", True)
        self.sanitize = kw.pop("sanitize", True)
        self.validate_only = kw.pop("validate_only", False)
        super().__init__(*args, **kw)

    def to_stdin(self):
        raise NotImplementedError

    def validate(self, answer):
        if self.answer:
            return self.answer == answer
        elif self.check_answer:
            return answer.validate(self)
        return True

    @classmethod
    def BaseAnswer(cls):
        attr = "_{}_BaseAnswer".format(cls.__name__)
        if not hasattr(cls, attr):
            class MyAnswerBase(BaseAnswer): pass
            setattr(cls, attr, MyAnswerBase)
        return getattr(cls, attr)

    @classmethod
    def Answer(cls):
        attr = "_{}_BaseAnswer".format(cls.__name__)
        base = getattr(cls, attr)
        for subcls in base.__subclasses__():
            return subcls
