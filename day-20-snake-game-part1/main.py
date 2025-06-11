from turtle import Screen, Turtle
import time

# 画面の設定
screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("Snake Game")
screen.tracer(0) # 画面の自動更新を無効化

# 蛇の初期化
snake_segments = []
positions = [(0, 0), (-20, 0), (-40, 0)]
for position in positions:
    new_segment = Turtle(shape="square")
    new_segment.color("white")
    new_segment.penup()
    new_segment.goto(position)
    snake_segments.append(new_segment)

# 入力に応じて蛇の向きを変える関数（逆方向には向けない）
def move_up():
    if snake_segments[0].heading() != 270:
        snake_segments[0].setheading(90)
def move_down():
    if snake_segments[0].heading() != 90:
        snake_segments[0].setheading(270)
def move_left():
    if snake_segments[0].heading() != 0:
        snake_segments[0].setheading(180)
def move_right():
    if snake_segments[0].heading() != 180:
        snake_segments[0].setheading(0)

# 方向キー入力の受付
screen.listen()
screen.onkey(key="Up", fun=move_up)
screen.onkey(key="Down", fun=move_down)
screen.onkey(key="Left", fun=move_left)
screen.onkey(key="Right", fun=move_right)

# 蛇の移動
game_is_on = True
while game_is_on:
    screen.update() # 画面の手動更新
    time.sleep(0.1)
    # 蛇の後ろから前に向かって移動
    for seg_num in range(len(snake_segments) - 1, 0, -1):
        new_x = snake_segments[seg_num - 1].xcor()
        new_y = snake_segments[seg_num - 1].ycor()
        snake_segments[seg_num].goto(new_x, new_y)
    # 蛇の先頭を移動
    snake_segments[0].forward(20)

screen.exitonclick()