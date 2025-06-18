from turtle import Turtle
import random


class Food(Turtle):
    """
    食べ物オブジェクトを表すクラス。
    画面上にランダムな位置に配置され、蛇が食べると新しい位置に移動します。
    """

    def __init__(self):
        super().__init__()
        self.shape("square")  # 形状を四角形に設定
        self.penup()  # ペンアップ（描画を無効にする）
        self.shapesize(stretch_wid=0.5, stretch_len=0.5)  # サイズを半分に縮小
        self.color("blue")  # 色を青に設定
        self.speed("fastest")  # 描画速度を最速に設定
        self.refresh()  # 初期位置を設定

    def refresh(self):
        """
        食べ物を画面上のランダムな位置に移動させます。
        """
        random_x = random.randint(-280, 280)
        random_y = random.randint(-280, 280)
        self.goto(random_x, random_y) 