"""

First building a representation of, and then solving the given sample logical puzzle below here.
Then creating 4 new similar puzzles having, respectively: 0, 1, 2, 3 solutions.

====================================================================================================
SAMPLE PUZZLE
====================================================================================================

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
import random
from hssrq import *


print()
print('=' * 100)
print('SOLVING THE SAMPLE PUZZLE')
print('=' * 100)
question_sequence = [
    FirstAnswerX('B', [1, 4, 3, 2]),
    AnswerToQuestionNr(4, ['D', 'A', 'B', 'C']),
    AnswerToQuestionNr(1, ['D', 'C', 'A', 'B']),
    CountOfAnswersX('D', [3, 2, 1, 0]),
    CountOfAnswersX('B', [0, 2, 3, 1]),
]
HomogeneousSequenceSelfReferentialQuestion.solve_puzzle(question_sequence, show=True)

for nr_solutions in range(0, 4):
    print()
    print('=' * 100)
    print(f'CREATING A NEW PUZZLE WITH {nr_solutions} SOLUTION{"S" if nr_solutions != 1 else ""}')
    print('=' * 100)
    new_question_sequence = HomogeneousSequenceSelfReferentialQuestion.create_puzzle(
        question_classes=[AnswerToQuestionNr, CountOfAnswersX, CountOfAnswersX, FirstAnswerX, LastAnswerX],
        nr_possible_answers=4,
        nr_solutions=nr_solutions
    )
