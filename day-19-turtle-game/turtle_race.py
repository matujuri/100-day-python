#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# プロジェクト: タートルレースゲーム
# ファイル名: turtle_race.py
# 目的: ユーザーが亀に賭けてレースを行うインタラクティブなゲームを実装する。
#       複数のタートルがランダムな速度で移動し、ゴールに到達したタートルが勝者となる。
#       ユーザーの賭けの結果に応じてメッセージを表示する。

import turtle
import random
import time

# --- 定数定義 ---
# スクリーンの幅 (ピクセル)
SCREEN_WIDTH = 500
# スクリーンの高さ (ピクセル)
SCREEN_HEIGHT = 400
# タートルがレースを開始するX座標
TURTLE_START_X = -230
# タートルがゴールと判定されるX座標
TURTLE_RACE_END_X = 200
# メッセージ表示のY座標 (画面中央)
MESSAGE_DISPLAY_Y = 0
# 賭けの入力時のメッセージ表示のY座標 (画面下部)
BET_MESSAGE_DISPLAY_Y = -100
# 通常のフォントスタイル (メッセージ表示用)
FONT = ("Arial", 16, "normal")
# 結果表示用のフォントスタイル (より大きく目立つように)
RESULT_FONT = ("Arial", 20, "normal")
# タートルの通常のサイズ
TURTLE_SIZE_NORMAL = 1
# 賭けたタートルや勝利したタートルを強調表示する際のサイズ
TURTLE_SIZE_LARGE = 2
# タートルが一度に進む最大距離 (ランダムウォークの最大値)
MOVE_DISTANCE_MAX = 10
# メッセージ表示後に待機する時間 (秒)
WAIT_TIME_AFTER_MESSAGE = 1.5
# 各タートル作成時の遅延時間 (アニメーション効果のため) (秒)
TURTLE_CREATION_DELAY = 0.1

# 日本語と英語の色名辞書
# キー: 英語の色名 (タートルモジュールで使用される)
# 値: 対応する日本語の色名 (ユーザー表示用)
COLOR_JP_NAME_DICT = {
    "red": "赤",
    "orange": "オレンジ",
    "yellow": "黄色",
    "green": "緑",
    "blue": "青",
    "purple": "紫"
}

# 亀の初期Y座標リスト
# レース開始時の各タートルのY座標を定義
Y_POSITIONS = [-70, -40, -10, 20, 50, 80]


# --- セットアップ関数 ---
# 目的: ゲームのスクリーンと結果表示タートルを初期設定する。
# 戻り値: screen (turtle.Screenオブジェクト), result_writer (turtle.Turtleオブジェクト)
def setup_game_elements():
    # スクリーンオブジェクトを作成し、サイズを設定
    screen = turtle.Screen()
    screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    
    # 結果メッセージ表示用のタートルを作成し、初期設定
    result_writer = turtle.Turtle()
    result_writer.hideturtle()  # タートル自身は非表示
    result_writer.penup()       # 線を描かずに移動
    result_writer.goto(0, MESSAGE_DISPLAY_Y) # 画面中央に設定
    result_writer.color("black") # メッセージの色
    return screen, result_writer

# 目的: 全てのカメを作成し、初期位置に配置する。
# 戻り値: all_turtles (作成されたturtle.Turtleオブジェクトのリスト)
def create_and_place_turtles():
    all_turtles = []
    turtle_colors = list(COLOR_JP_NAME_DICT.keys()) # 定義済みの色リストを取得
    # 各色に対応するタートルを作成
    for i, color in enumerate(turtle_colors):
        new_turtle = turtle.Turtle(shape="turtle") # タートル形状を設定
        new_turtle.penup() # 線を描かずに移動
        new_turtle.color(color) # タートルの色を設定
        all_turtles.append(new_turtle) # リストに追加
        time.sleep(TURTLE_CREATION_DELAY) # タートル作成ごとに短い遅延

    # カメを初期位置に配置（アニメーションを見せるため、後から作ったカメから順に配置）
    for i in range(len(all_turtles) - 1, -1, -1):
        new_turtle = all_turtles[i]
        new_turtle.goto(x=TURTLE_START_X, y=Y_POSITIONS[i])
    return all_turtles

# 目的: ユーザーから賭けの入力を受け付け、有効な色であることを検証する。
# 引数: screen (turtle.Screenオブジェクト), result_writer (メッセージ表示用turtle.Turtleオブジェクト)
# 戻り値: user_bet (ユーザーが賭けた亀の英語の色名)
def get_user_bet(screen, result_writer):
    user_bet = ""
    while True:
        # ユーザーに賭けの入力を促すダイアログを表示
        input_bet_raw = screen.textinput(title="亀に賭けよう！", prompt="どの亀に賭けますか？ (赤, オレンジ, 黄色, 緑, 青, 紫)")

        if input_bet_raw is None:
            # ユーザーがキャンセルした場合
            print("入力をキャンセルしました。ゲームを終了します。")
            screen.bye() # スクリーンを閉じる
            exit() # プログラムを終了

        # 入力された文字列の前後の空白を削除し、小文字に変換して正規化
        trimmed_input = input_bet_raw.strip().lower()

        # 入力された色が有効な色名（英語または日本語）であるかチェック
        for eng_color, jp_name in COLOR_JP_NAME_DICT.items():
            if trimmed_input == eng_color or trimmed_input == jp_name:
                user_bet = eng_color # 有効な場合は英語の色名を設定
                break

        if user_bet:
            # 有効な色の場合はループを抜ける
            break
        else:
            # 無効な色の場合は画面にエラーメッセージを表示
            result_writer.clear() # 前のメッセージをクリア
            result_writer.goto(0, BET_MESSAGE_DISPLAY_Y) # メッセージ表示位置を調整
            result_writer.write("無効な色です。もう一度入力してください。", align="center", font=FONT)
            time.sleep(WAIT_TIME_AFTER_MESSAGE) # メッセージ表示時間
            result_writer.clear() # メッセージをクリア
            result_writer.goto(0, MESSAGE_DISPLAY_Y) # メッセージ表示位置を元に戻す
    return user_bet

# 目的: タートルレースを開始し、勝者を決定する。
# 引数: all_turtles (レースに参加するturtle.Turtleオブジェクトのリスト)
# 戻り値: winning_color (勝利した亀の英語の色名、レースが終了しなかった場合はNone)
def run_race(all_turtles):
    is_race_on = True # レースが進行中かを示すフラグ
    while is_race_on:
        # 各タートルがランダムに前進
        for turtle_obj in all_turtles:
            rand_distance = random.randint(0, MOVE_DISTANCE_MAX) # 0から最大距離までのランダムな移動量
            turtle_obj.forward(rand_distance) # タートルを移動させる

            # タートルがゴールラインを超えたかチェック
            if turtle_obj.xcor() > TURTLE_RACE_END_X:
                is_race_on = False # レースを終了
                return turtle_obj.pencolor() # 勝者の色を返す
    return None # レースが何らかの理由で終了しなかった場合（通常は発生しない想定）

# 目的: レース結果を画面に表示する。
# 引数: winning_color (勝利した亀の英語の色名), user_bet (ユーザーが賭けた亀の英語の色名),
#       result_writer (メッセージ表示用turtle.Turtleオブジェクト)
# 戻り値: なし
def display_result(winning_color, user_bet, result_writer):
    # 勝者の英語の色名を日本語に変換
    winning_color_japanese = COLOR_JP_NAME_DICT[winning_color]
    message = ""
    # 賭けが当たったかどうかに応じてメッセージを生成
    if winning_color == user_bet:
        message = f"おめでとうございます！\nあなたが賭けた{winning_color_japanese}の亀が勝ちました！"
    else:
        message = f"残念！あなたが賭けた亀は勝ちませんでした。\n{winning_color_japanese}の亀が勝ちました！"

    result_writer.clear() # 前のメッセージをクリア
    result_writer.goto(0, MESSAGE_DISPLAY_Y) # 中央に表示
    result_writer.write(message, align="center", font=RESULT_FONT) # メッセージを表示


# --- メインゲームフロー ---
# 目的: ゲームの開始から終了までの全体の流れを制御する。
# 処理内容:
# 1. ゲーム要素 (スクリーン, 結果表示用タートル) のセットアップ
# 2. レース参加タートルの作成と初期配置
# 3. ユーザーからの賭けの入力を受け付け
# 4. ユーザーが賭けたタートルの強調表示
# 5. レースの実行
# 6. レース結果の表示と勝者タートルの強調表示

screen, result_writer = setup_game_elements()
all_turtles = create_and_place_turtles()
user_bet = get_user_bet(screen, result_writer)

# 賭けたカメを一時的に大きく表示する処理
bet_turtle = None
for turtle_obj in all_turtles:
    if turtle_obj.pencolor() == user_bet:
        bet_turtle = turtle_obj
        bet_turtle.turtlesize(TURTLE_SIZE_LARGE, TURTLE_SIZE_LARGE, TURTLE_SIZE_LARGE) # 大きくする
        time.sleep(WAIT_TIME_AFTER_MESSAGE) # 一定時間待機
        bet_turtle.turtlesize(TURTLE_SIZE_NORMAL, TURTLE_SIZE_NORMAL, TURTLE_SIZE_NORMAL) # 元に戻す
        break

result_writer.clear() # レース開始前に表示されている可能性のあるメッセージをクリア

winning_color = run_race(all_turtles) # レースを実行し、勝者の色を取得

if winning_color:
    display_result(winning_color, user_bet, result_writer) # 結果メッセージを表示
    
    # 勝利したカメを大きく表示する処理
    for turtle_obj in all_turtles:
        if turtle_obj.pencolor() == winning_color:
            turtle_obj.turtlesize(TURTLE_SIZE_LARGE, TURTLE_SIZE_LARGE, TURTLE_SIZE_LARGE) # 勝利したカメを強調
            break

screen.exitonclick() # クリックで画面を閉じる
