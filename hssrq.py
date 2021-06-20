import itertools
from helper_tools import *


class HomogeneousSequenceSelfReferentialQuestion:
    """
    A question whose correct answer depends only on the answers to a sequence of questions including itself,
    with each question in the sequence having the same number of possible answers and same answer labels.

    A list of questions of this type is collectively self-referential to itself, even though some single questions
    might be not self-referential individually.
    If the list of questions is properly chosen, then it will be a logical puzzle admitting just one list of answers.

    Example of such a puzzle with only one list of answers (also solved in the main):

    LOGICAL PUZZLE MADE UP BY COLLECTIVELY SELF-REFERENTIAL QUESTIONS

    1. The first question with B as the correct answer is:
        A. 1    B. 4    C. 3    D. 2

    2. The answer to Question 4 is:
        A. D    B. A    C. B    D. C

    3. The answer to Question 1 is:
        A. D    B. C    C. A    D. B

    4. The number of questions which have D as the correct answer is:
        A. 3    B. 2    C. 1    D. 0

    5. The number of questions which have B as the correct answer is:
        A. 0    B. 2    C. 3    D. 1

    SOLUTION(S)

    --- List of all possible sequences of answers: ---
        1. C,   2. D,   3. B,   4. C,   5. B
    --- End of the list ---

    This puzzle has exactly 1 solution.

    """

    def __init__(self, func, text, possible_answers, answer_labels=None):
        self.nr_possible_answers = len(possible_answers)
        if answer_labels is None:
            answer_labels = get_auto_labels(self.nr_possible_answers)
        else:
            assert len(answer_labels) == self.nr_possible_answers
        self.func = func
        self.text = text
        self.options = {pa: al for pa, al in zip(possible_answers, answer_labels)}

    def answer(self, all_right_answers):
        return self.options.get(self.func(all_right_answers))

    def get_full_text(self):
        sep = '    '
        return f'{self.text}:\n{sep}' \
               f'{sep.join([str(label) + ". " + str(answer) for answer, label in self.options.items()])}'

    @staticmethod
    def solve_puzzle(question_sequence, check=True, show=True):
        if check and not all([isinstance(question, HomogeneousSequenceSelfReferentialQuestion)
                              for question in question_sequence]):
            raise ValueError(f'All the list items must be instances of class '
                             f'{HomogeneousSequenceSelfReferentialQuestion.__class__.__name__}.')

        answer_labels = list(question_sequence[0].options.values())

        if check and not all([list(question.options.values()) == answer_labels for question in question_sequence[1:]]):
            raise ValueError(f'All the questions must have the same number of possible answers and answer labels')

        if show:
            print()
            print('LOGICAL PUZZLE MADE UP BY COLLECTIVELY SELF-REFERENTIAL QUESTIONS')
            print('')
            print('\n\n'.join([str(question_nr) + '. ' + question.get_full_text()
                               for question_nr, question in enumerate(question_sequence, 1)]))
            print()
            print('SOLUTION(S)')
            print('')
            print('--- List of all possible sequences of answers: ---')

        acceptable_answer_lists = []
        for answer_list in itertools.product(*([answer_labels] * len(question_sequence))):
            attempted_answers = []
            for question in question_sequence:
                try:
                    attempted_answer = question.answer(answer_list)
                except:
                    attempted_answer = None
                attempted_answers.append(attempted_answer)
            if all([attempted_answer == answer
                    for attempted_answer, answer in zip(attempted_answers, answer_list)]):
                acceptable_answer_lists.append(answer_list)
                if show: print('    ' + ',   '.join(f'{question_nr}. {answer_label}'
                                           for question_nr, answer_label in enumerate(answer_list, 1)))
        if show:
            print('--- End of the list ---')
            print('')
            nr_acceptable_answers = len(acceptable_answer_lists)
            if nr_acceptable_answers == 0:
                print('This puzzle has no solution.')
            elif nr_acceptable_answers == 1:
                print('This puzzle has exactly 1 solution.')
            else:
                print(f'This puzzle has {nr_acceptable_answers} possible solutions in total.')
            print()
        return answer_list


class AnswerToQuestionNr(HomogeneousSequenceSelfReferentialQuestion):
    def __init__(self, question_nr, possible_answers):
        super().__init__(
            func=lambda all_right_answers: all_right_answers[question_nr - 1],
            possible_answers=possible_answers,
            text=f'The answer to Question {question_nr} is'
        )


class CountOfAnswersX(HomogeneousSequenceSelfReferentialQuestion):
    def __init__(self, answer_label_x, possible_answers):
        super().__init__(
            func=lambda all_right_answers: all_right_answers.count(answer_label_x),
            possible_answers=possible_answers,
            text=f'The number of questions which have {answer_label_x} as the correct answer is'
        )


class FirstAnswerX(HomogeneousSequenceSelfReferentialQuestion):
    def __init__(self, answer_label_x, possible_answers):
        super().__init__(
            func=lambda all_right_answers: index_in_list(answer_label_x, all_right_answers) + 1,
            possible_answers=possible_answers,
            text=f'The first question with {answer_label_x} as the correct answer is'
        )


class LastAnswerX(HomogeneousSequenceSelfReferentialQuestion):
    def __init__(self, answer_label_x, possible_answers):
        super().__init__(
            func=lambda all_right_answers: index_in_list(answer_label_x, all_right_answers, -1) + 1,
            possible_answers=possible_answers,
            text=f'The last question with {answer_label_x} as the correct answer is'
        )
