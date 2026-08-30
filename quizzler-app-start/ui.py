from tkinter import  *

from quiz_brain import QuizBrain

THEME_COLOR = "#375362"

class QuizInterface:

    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.title("Quizzler")

        self.window.config(bg=THEME_COLOR, padx=20, pady=20)

        # score
        self.score = Label(text="Score: 0", fg="white", bg=THEME_COLOR)
        self.score.grid(column=1, row=0)

        # question
        self.question_canvas = Canvas(width=300, height=250, bg="white")
        self.question = self.question_canvas.create_text(
            150, 125,
            fill=THEME_COLOR,
            text="Some question text",
            font=("Arial", 20, "italic"),
            width=280)
        self.question_canvas.grid(column=0, row=1, columnspan=2, pady=50)

        # true (check) button
        true_image = PhotoImage(file="images/true.png")
        self.true_button = Button(image=true_image, highlightthickness=0, borderwidth=0, command=self.true_pressed)
        self.true_button.grid(column=0, row=2)

        # false (x) button
        false_image = PhotoImage(file="images/false.png")
        self.false_button = Button(image=false_image, highlightthickness=0, borderwidth=0, command=self.false_pressed)
        self.false_button.grid(column=1, row=2)

        self.get_next_question()

        self.window.mainloop()

    def true_pressed(self):
        is_right = self.quiz.check_answer("True")
        self.give_feedback(is_right)

    def false_pressed(self):
        is_right = self.quiz.check_answer("False")
        self.give_feedback(is_right)

    def get_next_question(self):
        self.question_canvas.config(bg="white")

        if self.quiz.still_has_questions():
            # update the score
            self.score.config(text=f"Score: {self.quiz.score}")

            q_text = self.quiz.next_question()
            self.question_canvas.itemconfig(self.question, text=q_text)
        else:
            self.question_canvas.itemconfig(self.question, text="You've reached the end of the quiz.")

            # disable buttons
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")

    def give_feedback(self, is_right):
        # change background to red if wrong, green if right
        # after one second change back to white
        if is_right:
            self.question_canvas.config(bg="green")
        else:
            self.question_canvas.config(bg="red")

        # set color back to white
        self.window.after(1000, self.get_next_question)

