from turtle import Screen
import time
from snake import Snake

# 画面のセットアップ
screen = Screen()  # Screenオブジェクトを作成
screen.setup(width=600, height=600)  # 画面のサイズを設定
screen.bgcolor("black")  # 背景色を黒に設定
screen.title("Snake Game")  # 画面のタイトルを設定
screen.tracer(0)  # 画面の自動更新を無効化（手動で更新するため）

# 蛇の初期化
snake = Snake()  # Snakeクラスの新しいインスタンスを作成

# キーボード入力のイベントリスナーを設定
screen.listen()  # キーボード入力を受け付けるように設定
screen.onkey(key="Up", fun=snake.up)  # "Up"キーが押されたときにsnake.upメソッドを呼び出す
screen.onkey(key="Down", fun=snake.down)  # "Down"キーが押されたときにsnake.downメソッドを呼び出す
screen.onkey(key="Left", fun=snake.left)  # "Left"キーが押されたときにsnake.leftメソッドを呼び出す
screen.onkey(key="Right", fun=snake.right)  # "Right"キーが押されたときにsnake.rightメソッドを呼び出す

# ゲームのメインループ
game_is_on = True  # ゲームが実行中であることを示すフラグ
while game_is_on:
    screen.update()  # 画面を更新して蛇の動きを表示
    time.sleep(0.1)  # 0.1秒間一時停止し、ゲームの速度を制御
    snake.move()  # 蛇を移動させる

screen.exitonclick()  # 画面がクリックされたときにゲームを終了する