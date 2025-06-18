from turtle import Turtle

class Paddle(Turtle):
    def __init__(self, position):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=1, stretch_len=5)
        self.penup()
        self.goto(position)
        self.setheading(90)
        
    def move_up(self):
        self.forward(20)
        
    def move_down(self):
        self.backward(20)