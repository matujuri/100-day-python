from turtle import Turtle, Screen
import random

tim = Turtle()
tim.shape("turtle")
tim.speed(0)
tim.pensize(10)

screen = Screen()
screen.setup(width=600, height=600)
screen.colormode(255)

directions = [0, 90, 180, 270]

def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)

def limit_space(x, y):
    current_x = tim.xcor()
    current_y = tim.ycor()
    if current_x > x or current_x < -x or current_y > y or current_y < -y:
        target_angle = tim.towards(0, 0)
        normalized_angle = (target_angle + 360) % 360
        closest_allowed_angle = round(normalized_angle / 90) * 90
        tim.setheading(closest_allowed_angle)

def random_walk():
    limit_space(300, 300)
    
    tim.color(random_color())
    tim.forward(50)
    tim.right(random.choice(directions))
    
for i in range(1000):
    random_walk()

screen.exitonclick()