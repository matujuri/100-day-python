import pandas as pd

data = pd.read_csv("2018_Central_Park_Squirrel_Census_-_Squirrel_Data_20250623.csv")

fur_color_count = data["Primary Fur Color"].value_counts()

fur_color_count.to_csv("squirrel_count.csv")