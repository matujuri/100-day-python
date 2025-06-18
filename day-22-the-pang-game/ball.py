from turtle import Turtle

SPEED = 0.1

class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.x_move = 10
        self.y_move = 10
        self.move_speed = SPEED
        
    def move(self):
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)
        
    def increase_speed(self):
        self.move_speed *= 0.9
        
    def bounce_y(self):
        self.y_move *= -1
        self.increase_speed()
        
    def bounce_x(self):
        self.x_move *= -1
        self.increase_speed()
        
    def reset_position(self):
        self.goto(0, 0)
        self.bounce_x() # 勝った方に向かってボールを打つ
        self.move_speed = SPEED