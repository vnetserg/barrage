from .baselauncher import BaseLauncher

class BaseTestCases(BaseLauncher):
    def handle_problem_set(self, name, problems):
        for i, prob in enumerate(problems):
            answer_got = self.get_answer(prob, name, i, len(problems))
            if not answer_got:
                return False
            if not prob.validate(answer_got):
                if prob.validate_only:
                    print("\nFAILED. STDIN:\n{}\nGOT:\n{}"
                          .format(prob.to_stdin(), answer_got.to_stdout()))
                    return False
                try:
                    answer_expected = prob.Answer().for_problem(prob)
                except NotImplementedError:
                    print("\nFAILED. STDIN:\n{}\nGOT:\n{}"
                          .format(prob.to_stdin(), answer_got.to_stdout()))
                else:
                    print("\nFAILED. STDIN:\n{}\nEXPECTED:\n{}\nGOT:\n{}"
                          .format(prob.to_stdin(), answer_expected.to_stdout(), answer_got.to_stdout()))
                return False
        print("")
        return True
    
