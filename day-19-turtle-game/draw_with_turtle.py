from turtle import Turtle, Screen


# タートルオブジェクトの初期設定
timmy = Turtle()
timmy.shape("turtle")
timmy.color("orange")
timmy.penup() # 線を描かずに移動
timmy.goto(0, 0) # 初期位置を原点に設定
timmy.pendown() # 線を描く準備

# 前に進む関数
# 目的: タートルを10ピクセル前方に移動させる
def move_forwards():
    timmy.forward(10)

# 後ろに進む関数
# 目的: タートルを10ピクセル後方に移動させる
def move_backwards():
    timmy.backward(10)

# 左に曲がる関数
# 目的: タートルを反時計回りに10度回転させる
def turn_left():
    timmy.left(10)

# 右に曲がる関数
# 目的: タートルを時計回りに10度回転させる
def turn_right():
    timmy.right(10)
    
# 画面をクリアしてタートルを初期位置に戻す関数
# 目的: 描画をすべて消去し、タートルをホームポジション（原点）に戻す
def clear_screen():
    timmy.clear() # 描画をクリア
    timmy.penup() # 線を描かずに移動
    timmy.home() # ホームポジションに戻る
    timmy.pendown() # 線を描く準備

# スクリーンとキーイベントの初期設定を行う関数
def setup_screen_and_listeners():
    screen = Screen()
    screen.listen() # キー入力を受け付けるように設定
    # 各キーに対応する関数を割り当てる
    screen.onkey(key="Up", fun=move_forwards)
    screen.onkey(key="Down", fun=move_backwards)
    screen.onkey(key="Left", fun=turn_left)
    screen.onkey(key="Right", fun=turn_right)
    screen.onkey(key="c", fun=clear_screen)
    return screen

screen = setup_screen_and_listeners()
screen.exitonclick()