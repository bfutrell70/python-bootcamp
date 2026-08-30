from operator import truediv

from question_model import Question
from data import question_data
from quiz_brain import QuizBrain

question_bank = []
for question in question_data:
    # Question(question_text=question['text'], question_answer=question['answer'])
    question_bank.append(
        Question(question_text=question['question'], question_answer=question['correct_answer'])
    )

# print(len(question_bank))

quiz_brain = QuizBrain(question_bank)

# print(quiz_brain.next_question())
while quiz_brain.still_has_questions():
    quiz_brain.next_question()

print(f"You've completed the quiz!")
print(f"Your final score was: {quiz_brain.score}/{quiz_brain.question_number} ")