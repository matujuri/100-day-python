from turtle import Turtle, Screen
import pandas as pd
import time

screen = Screen()
screen.title("Japan Map Quiz")
screen.setup(width=1200, height=1250)
image = "japan_map.gif"
screen.addshape(image)
t = Turtle()
t.shape(image)

data = pd.read_csv("47_todofuken.csv")
writer = Turtle()
writer.penup()
writer.hideturtle()

guessed_todofuken = []
todofuken_to_learn = []
while len(guessed_todofuken) < 47:
    input_todofuken = screen.textinput(title=f"{len(guessed_todofuken)}/47 都道府県名を当てるゲーム", prompt="都道府県名を入力してください。終了する場合は'exit'と入力してください。").strip().title()
    if input_todofuken.title() == "Exit":
        for todofuken in data.日本語名.values:
            if todofuken not in guessed_todofuken:
                todofuken_to_learn.append([todofuken, data[data.日本語名 == todofuken].英語名.item()])
        pd.DataFrame(todofuken_to_learn).to_csv(f"todofuken_to_learn_{time.strftime('%Y%m%d_%H%M%S')}.csv")
        break

    if input_todofuken in data.日本語名.values:
        todofuken_data = data[data.日本語名 == input_todofuken]
        writer.goto(todofuken_data.x.item(), todofuken_data.y.item())
        writer.write(todofuken_data.日本語名.item())
        guessed_todofuken.append(todofuken_data.日本語名.item())
        
    if input_todofuken.title() in data.英語名.values:
        todofuken_data = data[data.英語名 == input_todofuken.title()]
        writer.goto(todofuken_data.x.item(), todofuken_data.y.item())
        writer.write(todofuken_data.日本語名.item())
        guessed_todofuken.append(todofuken_data.日本語名.item())

if len(guessed_todofuken) == 47:
    writer.goto(0, 0)
    writer.write("Congratulations! You've guessed all 47 prefectures!", align="center", font=("Arial", 20, "bold"))

screen.exitonclick()
