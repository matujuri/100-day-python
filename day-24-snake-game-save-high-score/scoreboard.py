from turtle import Turtle

ALIGNMENT = "center"
FONT = ("Courier", 24, "normal")

class Scoreboard(Turtle):
    
    def __init__(self):
        super().__init__()
        self.score = 0
        self.color("white")
        self.penup()
        self.goto(0, 270)
        self.hideturtle()
        self.update_scoreboard()
        
    def update_scoreboard(self):
        self.clear()
        self.write(f"Score: {self.score}", align=ALIGNMENT, font=FONT)
        
    def game_over(self):
        self.goto(0, 0)
        self.write("GAME OVER", align=ALIGNMENT, font=FONT)
        # ゲームオーバー時に再プレイの選択肢を表示
        self.goto(0, -50)
        self.write("Press 'y' to play again, 'n' to exit.", align=ALIGNMENT, font=FONT)

    # スコアボードをリセットするメソッド
    def reset_scoreboard(self):
        self.score = 0
        self.goto(0, 270)
        self.update_scoreboard()
        
    def increase_score(self):
        self.score += 1
        self.update_scoreboard()