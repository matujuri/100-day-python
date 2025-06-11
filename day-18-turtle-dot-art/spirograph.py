from turtle import Turtle, Screen
import random


# タートルとスクリーンの初期設定を行う関数
def setup_turtle_and_screen():
    tim = Turtle()
    tim.shape("turtle")
    tim.speed(0)  # 最速に設定

    screen = Screen()
    screen.setup(width=600, height=600) # スクリーンサイズを設定
    screen.colormode(255) # カラーモードをRGBに設定
    return tim, screen

tim, screen = setup_turtle_and_screen()


# ランダムな色を生成する関数
# 目的: RGB値に基づいてランダムなタプルの色を生成する
# 戻り値: (r, g, b)形式の色のタプル
def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    random_color_tuple = (r, g, b)
    return random_color_tuple

# スパイログラフを描画する関数
# 目的: 指定された隙間のサイズに基づいて円を複数描き、スパイログラフを形成する
# 引数: size_of_gap (円間の角度の隙間)
def draw_spirograph(size_of_gap):
    # 360度をsize_of_gapで割った回数だけ円を描画
    for _ in range(int(360 / size_of_gap)):
        tim.color(random_color()) # ランダムな色を設定
        tim.circle(100) # 半径100の円を描画
        tim.setheading(tim.heading() + size_of_gap) # 次の円のために向きを変更

# スパイログラフを描画（隙間サイズを5度として呼び出し）
draw_spirograph(5)

# クリックで画面を閉じる
screen.exitonclick()

