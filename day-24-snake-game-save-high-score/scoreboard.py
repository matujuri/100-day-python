from turtle import Turtle

ALIGNMENT = "center"
FONT = ("Courier", 24, "normal")

class Scoreboard(Turtle):
    
    def __init__(self):
        super().__init__()
        self.score = 0
        self.high_score = self.get_high_score()
        self.color("white")
        self.penup()
        self.goto(0, 270)
        self.hideturtle()
        self.update_scoreboard()
        
    def get_high_score(self):
        with open("data.txt", mode="r") as file:
            return int(file.read())
        
    def set_high_score(self, score):
        with open("data.txt", mode="w") as file:
            file.write(str(score))
        
    def update_scoreboard(self):
        self.clear()
        self.write(f"Score: {self.score} High Score: {self.high_score}", align=ALIGNMENT, font=FONT)
        
    def game_over(self):
        self.goto(0, 0)
        self.write("GAME OVER", align=ALIGNMENT, font=FONT)
        # ゲームオーバー時に再プレイの選択肢を表示
        self.goto(0, -50)
        self.write("Press 'y' to play again, 'n' to exit.", align=ALIGNMENT, font=FONT)

    # スコアボードをリセットするメソッド
    def reset_scoreboard(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.set_high_score(self.high_score)
        self.score = 0
        self.goto(0, 270)
        self.update_scoreboard()
        
    def increase_score(self):
        self.score += 1
        self.update_scoreboard()