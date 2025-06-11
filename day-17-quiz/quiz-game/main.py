#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ファイル名: main.py
# 目的: クイズゲームのメイン実行ファイル。質問データを読み込み、
#       クイズの質問オブジェクトを生成し、クイズロジックを管理する。
#       ユーザーの回答を受け付け、最終スコアを表示する。

from data import question_data
from question_model import Question
from quiz_brain import QuizBrain

# 質問オブジェクトを格納するリストを初期化
question_bank = []

# data.py から質問データを取得し、Questionオブジェクトを生成してquestion_bankに追加
# 目的: 辞書形式の質問データをQuestionオブジェクトに変換し、クイズで利用できるようにする。
for question in question_data:
    question_text = question["text"]
    question_answer = question["answer"]
    new_question = Question(question_text, question_answer)
    question_bank.append(new_question)

# QuizBrainオブジェクトを生成し、質問バンクを渡す
# 目的: クイズの進行、質問の出題、正誤判定、スコア管理を行う。
quiz = QuizBrain(question_bank)

# クイズにまだ質問が残っている間は次の質問を出題し続ける
# 目的: 全ての質問が出題されるまでクイズを続行する。
while quiz.still_has_questions():
    quiz.next_question()

# クイズ完了メッセージと最終スコアを表示
print("クイズが完了しました！")
print(f"あなたの最終スコアは: {quiz.score}/{quiz.question_number} でした")