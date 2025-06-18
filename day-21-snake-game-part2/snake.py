from turtle import Turtle

STARTING_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]  # 蛇の初期位置（3つのセグメント）
MOVE_DISTANCE = 20  # 蛇が1回で移動する距離
UP = 90  # 上方向の角度
DOWN = 270  # 下方向の角度
LEFT = 180  # 左方向の角度
RIGHT = 0  # 右方向の角度

class Snake:
    """
    蛇ゲームの蛇オブジェクトを表すクラス。
    セグメントの作成、移動、方向転換の機能を提供します。
    """

    def __init__(self):
        # 蛇の各セグメントを格納するリストを初期化します。
        self.segments = []
        # 蛇の初期セグメントを作成します。
        self.create_snake()
        # 蛇の頭（最初のセグメント）を識別します。
        self.head = self.segments[0]

    def create_snake(self):
        """
        指定された初期位置に基づいて、蛇の初期セグメントを作成します。
        各セグメントは正方形で白色で、ペンアップされています。
        """
        for position in STARTING_POSITIONS:
            # 新しいタートルオブジェクト（正方形）を作成します。
            new_segment = Turtle("square")
            # セグメントの色を白に設定します。
            new_segment.color("white")
            # セグメントを移動する際に線を描かないようにペンアップします。
            new_segment.penup()
            # セグメントを初期位置に移動させます。
            new_segment.goto(position)
            # 作成したセグメントをリストに追加します。
            self.segments.append(new_segment)
            
    def add_segment(self, position):
        new_segment = Turtle("square")
        new_segment.color("white")
        new_segment.penup()
        new_segment.goto(position)
        self.segments.append(new_segment)
        
    def extend(self):
        self.add_segment(self.segments[-1].position())

    def move(self):
        """
        蛇を移動させます。
        各セグメントは前のセグメントの位置に移動し、頭が前方に移動します。
        この部分は、蛇の体節が連結して動く様子を再現しています。
        """
        # 蛇の尻尾から頭に向かって移動します（最後のセグメントから2番目のセグメントまで）。
        for seg_num in range(len(self.segments) - 1, 0, -1):
            # 前のセグメントのX座標を取得します。
            new_x = self.segments[seg_num - 1].xcor()
            # 前のセグメントのY座標を取得します。
            new_y = self.segments[seg_num - 1].ycor()
            # 現在のセグメントを前のセグメントの位置に移動させます。
            self.segments[seg_num].goto(new_x, new_y)
        # 蛇の頭を前方に移動させます。
        self.head.forward(MOVE_DISTANCE)

    def up(self):
        """
        蛇の頭を上方向に向けます。
        ただし、現在の方向が下方向でない場合に限ります（逆方向には向けないようにすることで、蛇がUターンするのを防ぎます）。
        """
        if self.head.heading() != DOWN:
            self.head.setheading(UP)

    def down(self):
        """
        蛇の頭を下方向に向けます。
        ただし、現在の方向が上方向でない場合に限ります（逆方向には向けないようにすることで、蛇がUターンするのを防ぎます）。
        """
        if self.head.heading() != UP:
            self.head.setheading(DOWN)

    def left(self):
        """
        蛇の頭を左方向に向けます。
        ただし、現在の方向が右方向でない場合に限ります（逆方向には向けないようにすることで、蛇がUターンするのを防ぎます）。
        """
        if self.head.heading() != RIGHT:
            self.head.setheading(LEFT)

    def right(self):
        """
        蛇の頭を右方向に向けます。
        ただし、現在の方向が左方向でない場合に限ります（逆方向には向けないようにすることで、蛇がUターンするのを防ぎます）。
        """
        if self.head.heading() != LEFT:
            self.head.setheading(RIGHT)
