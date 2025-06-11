from turtle import Turtle, Screen
import random


# タートルとスクリーンの初期設定を行う関数
def setup_turtle_and_screen():
    tim = Turtle()
    tim.shape("turtle")
    tim.speed(0)  # 最速に設定
    tim.pensize(10) # ペンの太さを設定

    screen = Screen()
    screen.setup(width=600, height=600) # スクリーンサイズを設定
    screen.colormode(255) # カラーモードをRGBに設定
    return tim, screen

tim, screen = setup_turtle_and_screen()

directions = [0, 90, 180, 270] # 移動方向（0:東, 90:北, 180:西, 270:南）

# ランダムな色を生成する関数
# 目的: RGB値に基づいてランダムなタプルの色を生成する
# 戻り値: (r, g, b)形式の色のタプル
def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)

# タートルが指定された空間内に留まるように動きを制限する関数
# 目的: タートルが画面の境界を超えそうになった場合、中心方向へ向きを変える
# 引数: x (X軸の境界), y (Y軸の境界)
def limit_space(x, y):
    current_x = tim.xcor()
    current_y = tim.ycor()
    # タートルが境界を超えた場合
    if current_x > x or current_x < -x or current_y > y or current_y < -y:
        # 中心(0,0)へ向かう角度を計算
        target_angle = tim.towards(0, 0)
        # 角度を0-360度の範囲に正規化
        normalized_angle = (target_angle + 360) % 360
        # 最も近い90度単位の角度に丸める
        closest_allowed_angle = round(normalized_angle / 90) * 90
        # タートルの向きを設定
        tim.setheading(closest_allowed_angle)

# ランダムウォークの1ステップを実行する関数
# 目的: 色をランダムに変更し、ランダムな方向に少し進む
def perform_random_step():
    limit_space(300, 300) # 画面の範囲を制限
    
    tim.color(random_color()) # ランダムな色に変更
    tim.forward(50) # 50歩前進
    tim.setheading(random.choice(directions)) # ランダムな方向に90度回転
    
# 1000回ランダムウォークを実行
for _ in range(1000):
    perform_random_step()

screen.exitonclick()