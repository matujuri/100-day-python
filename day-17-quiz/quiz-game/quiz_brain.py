#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ファイル名: quiz_brain.py
# 目的: クイズゲームのロジックを管理するQuizBrainクラスを定義する。
#       質問の進行、ユーザーの回答のチェック、スコアの追跡を行う。

class QuizBrain:
    # 目的: QuizBrainオブジェクトを初期化する。
    # 引数:
    #   q_list (list): Questionオブジェクトのリスト (質問バンク)。
    def __init__(self, q_list):
        self.question_number = 0  # 現在の質問番号を追跡 (0から開始)
        self.question_list = q_list  # 質問のリスト
        self.score = 0  # ユーザーの正解数を追跡

    # 目的: まだ質問が残っているかどうかを判定する。
    # 戻り値: bool (質問が残っていればTrue、そうでなければFalse)。
    def still_has_questions(self):
        return self.question_number < len(self.question_list)

    # 目的: 次の質問を出題し、ユーザーからの回答を受け付ける。
    # 処理内容:
    #   現在の質問を取得し、質問番号をインクリメントする。
    #   質問文と正解/不正解の選択肢をユーザーに提示し、回答を待つ。
    #   受け取った回答をcheck_answerメソッドに渡して検証する。
    def next_question(self):
        current_question = self.question_list[self.question_number] # 現在の質問オブジェクトを取得
        self.question_number += 1 # 質問番号を1つ進める
        user_answer = input(f"Q.{self.question_number}: {current_question.text} (True/False): ") # ユーザーからの入力を受け付ける
        self.check_answer(user_answer, current_question.answer) # 回答をチェックする

    # 目的: ユーザーの回答が正しいかどうかをチェックし、スコアを更新する。
    # 引数:
    #   user_answer (str): ユーザーが入力した回答。
    #   correct_answer (str): 現在の質問の正解。
    # 処理内容:
    #   ユーザーの回答と正解を比較し、正しければスコアを加算する。
    #   正誤判定の結果と現在のスコアをユーザーに表示する。
    def check_answer(self, user_answer, correct_answer):
        if user_answer.lower() == correct_answer.lower(): # 回答を小文字に変換して比較
            self.score += 1 # 正解ならスコアを加算
            print("正解です！")
        else:
            print("不正解です。")
        print(f"正解は: {correct_answer} でした。")
        print(f"現在のスコアは: {self.score}/{self.question_number} です")
        print("\n") # 区切りのための改行