from turtle import Turtle, Screen
import pandas as pd
import time

screen = Screen()
screen.title("China Map Quiz")
screen.setup(width=1000, height=1000)
screen.bgpic("china_blank.gif")

data = pd.read_csv("china_provinces.csv")
writer = Turtle()
writer.penup()
writer.hideturtle()

guessed_provinces = []
provinces_to_learn = []
while len(guessed_provinces) < 34:
    input_province = screen.textinput(title=f"{len(guessed_provinces)}/34 猜省份名称", prompt="输入省份名称。结束时输入'exit'。").strip().title()
    if input_province.title() == "Exit":
        provinces_to_learn = [province for province in data.中文名称.values if province not in guessed_provinces]
        pd.DataFrame(provinces_to_learn).to_csv(f"provinces_to_learn_{time.strftime('%Y%m%d_%H%M%S')}.csv")
        break

    if input_province in data.中文名称.values:
        province_data = data[data.中文名称 == input_province]
        writer.goto(province_data.x.item(), province_data.y.item())
        writer.write(province_data.中文名称.item())
        guessed_provinces.append(province_data.中文名称.item())
        
    if input_province.title() in data.英文名称.values:
        province_data = data[data.英文名称 == input_province.title()]
        writer.goto(province_data.x.item(), province_data.y.item())
        writer.write(province_data.中文名称.item())
        guessed_provinces.append(province_data.中文名称.item())

if len(guessed_provinces) == 34:
    writer.goto(0, 0)
    writer.write("恭喜你，你猜对了所有省份！", align="center", font=("Arial", 20, "bold"))

screen.exitonclick()