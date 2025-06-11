#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ファイル名: question_model.py
# 目的: クイズの個々の質問を表現するためのQuestionクラスを定義する。
#       各質問には質問文と正解が関連付けられる。

class Question:
    # 目的: Questionオブジェクトを初期化する。
    # 引数:
    #   text (str): 質問のテキスト。
    #   answer (str): 質問の正解 (True/False)。
    def __init__(self, text, answer):
        self.text = text    # 質問文を格納
        self.answer = answer # 正解を格納