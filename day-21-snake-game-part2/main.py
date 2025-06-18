from turtle import Screen
import time
from snake import Snake
from food import Food
from scoreboard import Scoreboard

# 画面のセットアップ
screen = Screen()  # Screenオブジェクトを作成
screen.setup(width=600, height=600)  # 画面のサイズを設定
screen.bgcolor("black")  # 背景色を黒に設定
screen.title("Snake Game")  # 画面のタイトルを設定
screen.tracer(0)  # 画面の自動更新を無効化（手動で更新するため）

# 蛇の初期化
snake = Snake()
food = Food()
scoreboard = Scoreboard()

# キーボード入力のイベントリスナーを設定 (初期設定)
screen.listen()  # キーボード入力を受け付けるように設定
screen.onkey(snake.up, "Up")  # "Up"キーが押されたときにsnake.upメソッドを呼び出す
screen.onkey(snake.down, "Down")  # "Down"キーが押されたときにsnake.downメソッドを呼び出す
screen.onkey(snake.left, "Left")  # "Left"キーが押されたときにsnake.leftメソッドを呼び出す
screen.onkey(snake.right, "Right")  # "Right"キーが押されたときにsnake.rightメソッドを呼び出す

game_continues = True # アプリケーション全体が継続するかどうかを制御
game_is_on = True     # 現在のゲームラウンドが進行中かどうかを制御

# ゲームをリスタートさせる関数
def restart_game():
    global game_is_on
    game_is_on = True  # ゲームラウンドを再開
    scoreboard.reset_scoreboard() # スコアボードをリセット
    snake.reset()      # 蛇をリセット
    food.refresh()     # 食べ物を再配置
    # 再開後のキーバインドをスネーク移動に戻す
    screen.onkey(snake.up, "Up")
    screen.onkey(snake.down, "Down")
    screen.onkey(snake.left, "Left")
    screen.onkey(snake.right, "Right")
    # y/nキーのバインドを解除
    screen.onkey(None, "y")
    screen.onkey(None, "n")

# ゲームを終了させる関数
def exit_game():
    global game_continues
    game_continues = False # アプリケーションを終了
    screen.bye() # ゲームウィンドウを閉じる

# ゲームのメインループ
while game_continues:
    screen.update()
    while game_is_on: # ゲームが進行中の場合のみ更新
        screen.update()
        time.sleep(0.1)
        snake.move()

        # 食べ物との衝突を検出
        if snake.head.distance(food) < 15:
            food.refresh()
            snake.extend()  # 蛇を拡張
            scoreboard.increase_score()

        # 壁との衝突を検出
        if snake.head.xcor() > 280 or snake.head.xcor() < -280 or snake.head.ycor() > 280 or snake.head.ycor() < -280:
            game_is_on = False
            scoreboard.game_over()
            # ゲームオーバー時のみy/nキーをバインド
            screen.onkey(restart_game, "y")
            screen.onkey(exit_game, "n")
    
    # game_is_on が False になったら、ゲームループを一時停止し、ユーザーのy/n入力を待機
    # screen.exitonclick() が screen.mainloop() と同じようにイベントループに入るため、
    # ここでさらに明示的なループは不要。
    # yまたはnが押されるまで、プログラムは自動的に待機する。

# アプリケーションの終了イベントループ
# screen.bye()が呼ばれるか、ウィンドウが閉じられるまでイベントを処理
screen.exitonclick()