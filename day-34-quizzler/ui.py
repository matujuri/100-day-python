from tkinter import Canvas, Tk, PhotoImage, Button, Label
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"

class QuizInterface:
    def __init__(self, quiz: QuizBrain):
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)
        self.quiz = quiz

        self.score_label = Label(text=f"Score: {self.quiz.score}", fg="white", bg=THEME_COLOR)
        self.score_label.grid(row=0, column=1)
        
        self.canvas = Canvas(width=300, height=250, bg="white")
        self.question_text = self.canvas.create_text(
            150,
            125,
            text="",
            fill=THEME_COLOR,
            font=("Arial", 20, "italic"),
            width=280
        )
        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)
        
        true_image = PhotoImage(file="day-34-quizzler/images/true.png")
        self.true_button = Button(image=true_image, highlightthickness=0, borderwidth=0, command=self.true_pressed)
        self.true_button.grid(row=2, column=0)
        
        false_image = PhotoImage(file="day-34-quizzler/images/false.png")
        self.false_button = Button(image=false_image, highlightthickness=0, borderwidth=0, command=self.false_pressed)
        self.false_button.grid(row=2, column=1)
        
        self.get_next_question()
        
        self.window.mainloop()
        
    def get_next_question(self):
        if self.quiz.still_has_questions():
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
        else:
            self.canvas.itemconfig(self.question_text, text="You've reached the end of the quiz.")
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")
        
    def true_pressed(self):
        is_right = self.quiz.check_answer("True")
        self.score_label.config(text=f"Score: {self.quiz.score}")
        self.give_feedback(is_right)
        
    def false_pressed(self):
        is_right = self.quiz.check_answer("False")
        self.score_label.config(text=f"Score: {self.quiz.score}")
        self.give_feedback(is_right)
        
    def give_feedback(self, is_right: bool):
        if is_right:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")
            
        self.window.after(1000, self.get_next_question)
        self.window.after(1000, self.reset_canvas)
        
    def reset_canvas(self):
        self.canvas.config(bg="white")