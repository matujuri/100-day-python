from turtle import Turtle, Screen
import random

tim = Turtle()
tim.shape("turtle")
tim.speed(0)
tim.penup()

color_list = [
    (236, 35, 108),
    (145, 28, 66),
    (239, 75, 35),
    (7, 148, 95),
    (220, 171, 45),
    (183, 158, 47),
    (45, 191, 232),
    (28, 127, 194),
    (254, 223, 0),
    (125, 192, 78),
    (85, 27, 91),
    (243, 218, 56),
    (178, 40, 98),
    (44, 170, 114),
    (211, 132, 166),
    (206, 57, 35),
]

screen = Screen()
screen.colormode(255)

# ドットの描画開始位置を設定
tim.setheading(225)  # 左下を向く
tim.forward(300)      # 開始位置へ移動
tim.setheading(0)    # 右を向く

number_of_dots = 100

for dot_count in range(1, number_of_dots + 1):
    tim.dot(20, random.choice(color_list))  # 直径20
    tim.forward(50)

    if dot_count % 10 == 0:  # 10個のドットを描画したら、上の行に移動
        tim.setheading(90)   
        tim.forward(50)      
        tim.setheading(180)  
        tim.forward(50 * 10)  
        tim.setheading(0)    

tim.hideturtle()
screen.exitonclick()

