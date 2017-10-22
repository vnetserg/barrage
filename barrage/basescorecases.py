
from .baselauncher import BaseLauncher

class BaseScoreCases(BaseLauncher):
    def handle_problem_set(self, name, problems):
        scores = []
        print("Scoring answers for '{}'...".format(name), end='\r')
        for i, prob in enumerate(problems):
            answer_got = self.get_answer(prob, name, i, len(problems))
            if not answer_got:
                return False
            perfect_answer = prob.Answer().for_problem(prob)
            scores.append(answer_got.score_against(perfect_answer))
        avg_score = sum(scores)/len(scores)
        print("Average score for '{}': {}   ".format(name, avg_score))
        return True
