
import random
import resource
import subprocess

from inspect import ismethod


class BaseTestCases:
    TIME_LIMIT = 1 # seconds
    MEMORY_LIMIT = 512 # megabytes

    class ExitCodeError(Exception): pass
    class TimeLimitError(Exception): pass
    class MemoryLimitError(Exception): pass

    def __init__(self, Answer, app, app_san, seed=None):
        self.Answer = Answer
        self.app = app
        self.app_san = app_san
        self.seed = seed
        self.random = random.Random()

    @classmethod
    def case(cls, fun, name=None):
        wrapper = cls.value_to_list(fun)
        if not hasattr(cls, "_next_case"):
            cls._next_case = 1
        wrapper._case_counter = cls._next_case
        cls._next_case += 1
        if name:
            cls.set_test_name(wrapper, name)
        else:
            cls.set_test_name(wrapper, cls.get_test_name(fun))
        return wrapper

    @classmethod
    def repeat(cls, num):
        def decorator(fun):
            gen = cls.value_to_list(fun)
            def wrapper(*args, **kw):
                return sum((gen(*args, **kw) for _ in range(num)), [])
            return cls.case(wrapper, cls.get_test_name(fun))
        return decorator

    @classmethod
    def forin(cls, arg, iterable):
        def decorator(fun):
            gen = cls.value_to_list(fun)
            def wrapper(*args, **kw):
                res = []
                for x in iterable:
                    kw[arg] = x
                    res += gen(*args, **kw)
                return res
            return cls.case(wrapper, cls.get_test_name(fun))
        return decorator

    @classmethod
    def nochecks(cls, fun):
        gen = cls.value_to_list(fun)
        def wrapper(*args, **kw):
            res = gen(*args, **kw)
            for prob in res:
                prob.check_answer = False
                prob.sanitize = False
            return res
        return cls.case(wrapper, cls.get_test_name(fun))

    @classmethod
    def value_to_list(cls, fun):
        def wrapper(*args, **kw):
            res = fun(*args, **kw)
            if isinstance(res, list):
                return res
            return [res]
        return wrapper

    @staticmethod
    def case_number(fun):
        return getattr(fun, "_case_counter", None)

    @classmethod
    def set_test_name(cls, fun, name):
        fun._test_name = name
    
    @classmethod
    def get_test_name(cls, fun):
        return getattr(fun, "_test_name", fun.__name__)

    def random_array(self, length, lo, hi):
        return [self.random.randrange(lo, hi) for _ in range(length)]

    def random_array_polarized(self, length, lo, hi):
        array = self.random_array(length, lo, hi)
        return [(x if self.random.randrange(2) else -x) for x in array]

    def run(self, forever=False):
        keep_running = True
        while keep_running:
            print("RUNNING TESTS WITH SEED: {}".format(self.seed))
            for get_problems in self.problem_generators():
                print("Generating problems with '{}'".format(self.get_test_name(get_problems)), end="\r")
                self.random.seed(self.get_test_name(get_problems) + str(self.seed))
                problems = get_problems()
                for i, prob in enumerate(problems):
                    print("Problem set '{}': running {}/{}".format(
                          self.get_test_name(get_problems), i+1, len(problems)), end="\r")
                    try:
                        stdout = self.run_app_on(prob)
                    except self.ExitCodeError as exc:
                        print("\nNONZERO EXIT CODE. STDIN:\n{}\nSTDERR:\n{}".format(prob.to_stdin(), exc.args[0]))
                        return False
                    except self.TimeLimitError:
                        print("\nTIME LIMIT EXCEEDED. STDIN:\n{}".format(prob.to_stdin()))
                        return False
                    except self.MemoryLimitError:
                        print("\nMEMORY LIMIT EXCEEDED. STDIN:\n{}".format(prob.to_stdin()))
                        return False
                    if prob.check_answer:
                        answer_got = self.Answer.from_stdout(stdout)
                        if not answer_got.validate(prob):
                            try:
                                answer_expected = self.Answer.for_problem(prob)
                            except NotImplemented:
                                print("\nFAILED. STDIN:\n{}\nGOT:\n{}"
                                      .format(prob.to_stdin(), stdout))
                            else:
                                print("\nFAILED. STDIN:\n{}\nEXPECTED:\n{}\nGOT:\n{}"
                                      .format(prob.to_stdin(), answer_expected.to_stdout(), stdout))
                            return False
                print("")
            keep_running = forever
            self.seed = random.randrange(100000)
        return True

    def problem_generators(self):
        attrs = [getattr(self, name) for name in dir(self)]
        methods = [a for a in attrs if self.case_number(a)]
        return sorted(methods, key=self.case_number)

    def run_app_on(self, problem):
        def limit_memory():
            if not problem.sanitize:
                limit = self.MEMORY_LIMIT * 1024 * 1024
                resource.setrlimit(resource.RLIMIT_AS, (limit, limit))

        app = self.app if not problem.sanitize else self.app_san
        sp = subprocess.Popen([app], stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                              stdin=subprocess.PIPE, preexec_fn=limit_memory)
        try:
            out, err = sp.communicate(problem.to_stdin().encode("utf-8"), timeout=self.TIME_LIMIT)
        except TimeoutError:
            sp.kill()
            raise self.TimeLimitError
        out = out.decode("utf-8").strip()
        err = err.decode("utf-8").strip()
        if sp.returncode == -11:
            raise self.MemoryLimitError
        if sp.returncode != 0:
            raise self.ExitCodeError(err)
        return out
