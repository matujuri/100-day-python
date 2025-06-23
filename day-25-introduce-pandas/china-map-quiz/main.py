import turtle
import pandas as pd

# 中国の省のデータをCSVから読み込む
data = pd.read_csv("china_provinces.csv")

# 新しいタートルオブジェクトを作成し、テキストの書き込みに使用
name_writer = turtle.Turtle()
name_writer.hideturtle()
name_writer.penup()

def write_province_name(name, x_coor, y_coor):
    """
    指定された座標に省の名前をGUI上に書き込む。
    Args:
        name (str): 表示する省の名前。
        x_coor (int): X座標。
        y_coor (int): Y座標。
    """
    name_writer.goto(x_coor, y_coor)
    name_writer.write(name, align="center", font=("Arial", 8, "normal"))

def update_province_coordinates(province_name, x, y):
    """
    指定された省の座標を更新し、CSVファイルに保存する。
    Args:
        province_name (str): 更新対象の省の名前。
        x (int): 新しいX座標。
        y (int): 新しいY座標。
    Returns:
        bool: 更新が成功した場合はTrue、見つからなかった場合はFalse。
    """
    # 省名でデータを検索
    province_data = data[data["中文名称"] == province_name]
    if not province_data.empty:
        # 見つかった場合、x, y座標を更新してCSVに保存
        index = province_data.index[0]
        data.loc[index, "x"] = x
        data.loc[index, "y"] = y
        data.to_csv("china_provinces.csv", index=False)
        print(f"{province_name}の座標を({x}, {y})に更新しました。")
        return True
    else:
        # 省が見つからなかった場合
        print(f"'{province_name}'は見つかりませんでした。正確な省名を入力してください。")
        return False

def get_mouse_click_coor(x, y):
    """
    マウスのクリック座標を取得し、ユーザーに省の名前を入力させて座標を更新する。
    Args:
        x (int): クリックされたX座標。
        y (int): クリックされたY座標。
    """
    print(x, y)
    province_name = screen.textinput(title="省の確認", prompt="クリックした省の名前を入力してください:")
    if province_name:
        if update_province_coordinates(province_name, x, y):
            write_province_name(province_name, x, y)  # 座標更新が成功した場合のみ省名を表示

screen = turtle.Screen()
screen.title("China Map Quiz")
screen.setup(width=1000, height=1000)
screen.bgpic("china_city.gif")

screen.onscreenclick(get_mouse_click_coor)

screen.mainloop()