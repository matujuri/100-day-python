import turtle
import random
import time

screen = turtle.Screen()
screen.setup(width=500, height=400)

# 結果メッセージ表示用のTurtle
result_writer = turtle.Turtle()
result_writer.hideturtle()
result_writer.penup()
result_writer.goto(0, 0) # 画面中央に設定
result_writer.color("black") # メッセージの色

# キーはturtleモジュールが使用する英語の色名、値は日本語の色名
color_jp_name_dict = {
    "red": "赤",
    "orange": "オレンジ",
    "yellow": "黄色",
    "green": "緑",
    "blue": "青",
    "purple": "紫"
}
# 亀の位置
y_positions = [-70, -40, -10, 20, 50, 80]
# 亀のリスト
all_turtles = []

# 亀の作成
turtle_colors = list(color_jp_name_dict.keys())
for i, color in enumerate(turtle_colors):
    new_turtle = turtle.Turtle(shape="turtle")
    new_turtle.penup()
    new_turtle.color(color)
    all_turtles.append(new_turtle)
    time.sleep(0.1) # 亀の作成を見やすくするために0.1秒待つ

# 亀が1匹ずつ起点から定位置に移動するアニメーションを見せるため、後から作った亀から順に配置
for i in range(len(all_turtles) - 1, -1, -1):
    all_turtles[i].goto(x=-230, y=y_positions[i])

# ユーザーの賭けの入力 (英語もしくは日本語から変換された英語)
user_bet = ""
while True:
    input_bet_raw = screen.textinput(title="亀に賭けよう！", prompt="どの亀に賭けますか？")

    if input_bet_raw is None:
        print("入力をキャンセルしました。ゲームを終了します。")
        screen.bye()
        exit()

    trimmed_input = input_bet_raw.strip().lower() # 前後の空白を削除し、小文字に変換

    for eng_color, jp_name in color_jp_name_dict.items():
        # 入力が英語名または日本語名と一致するかチェック
        if trimmed_input == eng_color or trimmed_input == jp_name:
            user_bet = eng_color
            break

    if user_bet: # 有効な色の場合はループを抜ける
        break
    else:
        # 無効な色の場合は画面にメッセージを表示し、ループを継続
        result_writer.clear()
        result_writer.goto(0, -100) # 少し低い位置に表示
        result_writer.write("無効な色です。もう一度入力してください。", align="center", font=("Arial", 16, "normal"))
        time.sleep(1.5) # メッセージを表示する時間
        result_writer.clear() # メッセージをクリア
        result_writer.goto(0, 0) # 位置を元に戻す

# 賭けた亀は試合開始前に大きく表示される
bet_turtle = None
for turtle_obj in all_turtles:
    if turtle_obj.pencolor() == user_bet:
        bet_turtle = turtle_obj
        bet_turtle.turtlesize(2, 2, 2)
        time.sleep(1)
        bet_turtle.turtlesize(1, 1, 1)
        break

# レース開始前に念のためメッセージをクリア
result_writer.clear()

# 試合開始
is_race_on = True
while is_race_on:
    for turtle_obj in all_turtles:
        # 亀がランダムに移動する
        rand_distance = random.randint(0, 10) # 亀がランダムに移動する距離
        turtle_obj.forward(rand_distance) # 亀を移動させる

        # ゴールに到達した亀を検出して試合終了
        if turtle_obj.xcor() > 200:
            is_race_on = False
            winning_color = turtle_obj.pencolor()
            # 英語の色名を日本語に変換して表示
            winning_color_japanese = color_jp_name_dict[winning_color]

            message = ""
            if winning_color == user_bet:
                message = f"おめでとうございます！\nあなたが賭けた{winning_color_japanese}の亀が勝ちました！"
            else:
                message = f"残念！あなたが賭けた亀は勝ちませんでした。\n{winning_color_japanese}の亀が勝ちました！"

            # 画面にメッセージを表示
            result_writer.clear()
            result_writer.goto(0, 0) # 中央に表示
            result_writer.write(message, align="center", font=("Arial", 20, "normal"))

            # 勝利した亀に大きく表示
            turtle_obj.turtlesize(2, 2, 2)
            break # 試合終了

screen.exitonclick()
