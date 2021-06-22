import itertools
from helper_tools import *
import random


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
        """
        :param func: a function with this signature:
            all_right_answers: sequence of answer labels assumed correct --> label of correct answer to this question
        :param text: question text
        :param possible_answers: possible answers
        :param answer_labels: corresponding answer labels (defaulting to 'A', 'B', 'C'...)
        """
        self.nr_possible_answers = len(possible_answers)
        if answer_labels is None:
            answer_labels = get_auto_labels(self.nr_possible_answers)
        else:
            assert len(answer_labels) == self.nr_possible_answers
        self.func = func
        self.text = text
        self.options = {pa: al for pa, al in zip(possible_answers, answer_labels)}

    def answer(self, all_right_answers):
        """
        (try to) answer this question on the assumption that the given sequence of answers to all questions is correct
        :param all_right_answers: sequence of answer labels
        :return: correct answer to this question, as an answer label
        """
        return self.options.get(self.func(all_right_answers))

    def get_full_text(self):
        """
        :return: full text representing this question and its possible answers
        """
        sep = '    '
        return f'{self.text}:\n{sep}' \
               f'{sep.join([str(label) + ". " + str(answer) for answer, label in self.options.items()])}'

    @classmethod
    def create_randomly(cls, nr_questions, answer_labels, this_question_index):
        """
        Abstract factory method building a theoretically admissible question;
        implement this method in a concrete subclass to support creating puzzles with no solution.
        :param nr_questions: nr. of questions in the sequence
        :param answer_labels: all answer labels
        :param this_question_index: zero-based index of this question in the question sequence
        :return: new instance of this class
        """
        pass

    @classmethod
    def create_backwards(cls, all_right_answers, answer_labels, this_question_index):
        """
        factory method building a question compatible with a pre-defined sequence of right answers
        :param all_right_answers: sequence of right answers
        :param answer_labels: all answer labels
        :param this_question_index: zero-based index of this question in the question sequence
        :return: new instance of this class
        """
        specifics_dict, right_answer, all_possible_answers = \
            cls._init_backwards(all_right_answers, answer_labels, this_question_index)
        wrong_answers = [a for a in all_possible_answers if a != right_answer]
        random.shuffle(wrong_answers)
        right_answer_label = all_right_answers[this_question_index]
        possible_answers = [right_answer if al == right_answer_label else wrong_answers.pop() for al in answer_labels]
        specifics_dict['possible_answers'] = possible_answers
        return cls(**specifics_dict)

    @classmethod
    def _init_backwards(cls, all_right_answers, answer_labels, this_question_index):
        """
        Abstract method deriving class-specific initialization information from the puzzle solution parameters;
        implement this method in a concrete class to support creating puzzles with solution nr. > 0.
        :param all_right_answers: sequence of right answers
        :param answer_labels: all answer labels
        :param this_question_index: zero-based index of this question in the question sequence
        :return:
            right_answer,
            all_possible_answers := list of all conceivable answers,
            specifics_dict := dict of the specific input parameters needed to init this class
        """
        raise NotImplementedError()
        specifics_dict = None
        right_answer = None
        all_possible_answers = None
        return specifics_dict, right_answer, all_possible_answers

    @staticmethod
    def solve_puzzle(question_sequence, check=False, show=False):
        """
        brute-force find all possible solutions - if any - to the logical puzzle made up by the given question sequence
        :param question_sequence: a sequence of instances of HomogeneousSequenceSelfReferentialQuestion
        :param check: if true, validate the input before trying to solve
        :param show: if true, print out both the puzzle description and the solution(s)
        :return: list of puzzle solutions, each being a sequence of answer labels
        """
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
        return acceptable_answer_lists

    @staticmethod
    def create_puzzle(question_classes, nr_possible_answers, nr_solutions=1, answer_labels=None, show=False):
        """
        try to randomly create a puzzle, without validating whether it is possible or not
        :param question_classes: list of concrete subclasses of HomogeneousSequenceSelfReferentialQuestion
        :param nr_possible_answers: nr. of possible answers to each questions
        :param nr_solutions: nr. of desired solutions
        :param answer_labels: labels of the answers, optional; defaults to A, B, C...
        :param show: if True, show the candidate puzzles that have been eliminated
        :return: the question list of the found puzzle
        """
        if answer_labels is None:
            answer_labels = get_auto_labels(nr_possible_answers)
        else:
            assert nr_possible_answers == len(nr_possible_answers)
        nr_attempts = 0
        while True:
            nr_attempts += 1
            print(f'Attempt nr. {nr_attempts}...')
            random.shuffle(question_classes)
            all_right_answers = [random.choice(answer_labels) for _ in range(len(question_classes))]
            if nr_solutions == 0:
                question_sequence = [question_class.create_randomly(len(all_right_answers), answer_labels, i)
                                     for i, question_class in enumerate(question_classes)]
            else:
                question_sequence = [question_class.create_backwards(all_right_answers, answer_labels, i)
                                     for i, question_class in enumerate(question_classes)]
            solutions = HomogeneousSequenceSelfReferentialQuestion.solve_puzzle(question_sequence, show=show)
            if len(solutions) == nr_solutions:
                HomogeneousSequenceSelfReferentialQuestion.solve_puzzle(question_sequence, show=True)
                return question_sequence


class AnswerToQuestionNr(HomogeneousSequenceSelfReferentialQuestion):
    def __init__(self, question_nr, possible_answers):
        super().__init__(
            func=lambda all_right_answers: all_right_answers[question_nr - 1],
            possible_answers=possible_answers,
            text=f'The answer to Question {question_nr} is'
        )

    @classmethod
    def create_randomly(cls, nr_questions, answer_labels, this_question_index):
        return cls(
            question_nr=random.choice([i for i in range(nr_questions) if i != this_question_index]) + 1,
            possible_answers=answer_labels
        )

    @classmethod
    def _init_backwards(cls, all_right_answers, answer_labels, this_question_index):
        question_index = random.choice([i for i in range(len(all_right_answers)) if i != this_question_index])
        question_nr = question_index + 1
        specifics_dict = dict(question_nr=question_nr)
        right_answer = all_right_answers[question_index]
        all_possible_answers = answer_labels
        return specifics_dict, right_answer, all_possible_answers


class CountOfAnswersX(HomogeneousSequenceSelfReferentialQuestion):
    def __init__(self, answer_label_x, possible_answers):
        super().__init__(
            func=lambda all_right_answers: all_right_answers.count(answer_label_x),
            possible_answers=possible_answers,
            text=f'The number of questions which have {answer_label_x} as the correct answer is'
        )

    @classmethod
    def create_randomly(cls, nr_questions, answer_labels, this_question_index):
        return cls(
            answer_label_x=random.choice(answer_labels),
            possible_answers=random.sample(list(range(nr_questions + 1)), len(answer_labels))
        )

    @classmethod
    def _init_backwards(cls, all_right_answers, answer_labels, this_question_index):
        answer_label_x = random.choice(list(set(all_right_answers)))
        specifics_dict = dict(answer_label_x=answer_label_x)
        right_answer = all_right_answers.count(answer_label_x)
        all_possible_answers = list(range(len(all_right_answers) + 1))
        return specifics_dict, right_answer, all_possible_answers


class FirstAnswerX(HomogeneousSequenceSelfReferentialQuestion):
    def __init__(self, answer_label_x, possible_answers):
        super().__init__(
            func=lambda all_right_answers: index_in_list(answer_label_x, all_right_answers) + 1,
            possible_answers=possible_answers,
            text=f'The first question with {answer_label_x} as the correct answer is'
        )

    @classmethod
    def create_randomly(cls, nr_questions, answer_labels, this_question_index):
        return cls(
            answer_label_x=random.choice(answer_labels),
            possible_answers=random.sample(list(range(1, nr_questions + 1)), len(answer_labels))
        )

    @classmethod
    def _init_backwards(cls, all_right_answers, answer_labels, this_question_index):
        answer_label_x = random.choice(list(set(all_right_answers)))
        specifics_dict = dict(answer_label_x=answer_label_x)
        right_answer = index_in_list(answer_label_x, all_right_answers) + 1
        all_possible_answers = list(range(1, len(all_right_answers) + 1))
        return specifics_dict, right_answer, all_possible_answers


class LastAnswerX(HomogeneousSequenceSelfReferentialQuestion):
    def __init__(self, answer_label_x, possible_answers):
        super().__init__(
            func=lambda all_right_answers: index_in_list(answer_label_x, all_right_answers, -1) + 1,
            possible_answers=possible_answers,
            text=f'The last question with {answer_label_x} as the correct answer is'
        )

    @classmethod
    def create_randomly(cls, nr_questions, answer_labels, this_question_index):
        return cls(
            answer_label_x=random.choice(answer_labels),
            possible_answers=random.sample(list(range(1, nr_questions + 1)), len(answer_labels))
        )

    @classmethod
    def _init_backwards(cls, all_right_answers, answer_labels, this_question_index):
        answer_label_x = random.choice(list(set(all_right_answers)))
        specifics_dict = dict(answer_label_x=answer_label_x)
        right_answer = index_in_list(answer_label_x, all_right_answers, direction=-1) + 1
        all_possible_answers = list(range(1, len(all_right_answers) + 1))
        return specifics_dict, right_answer, all_possible_answers
