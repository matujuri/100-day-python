# import csv

# with open("weather_data.csv") as data_file:
#     data = csv.reader(data_file)
#     temperatures = []
#     for row in data:
#         if row[1] != "temp":
#             temperatures.append(int(row[1]))
#     print(temperatures)


import pandas as pd


# data: dataframe
data = pd.read_csv("weather_data.csv")
# data_dict = data.to_dict()
# print(data_dict)

# # data["temp"]: series
# temp_list = data["temp"].to_list()
# print(temp_list)

# # temp_mean = sum(temp_list) / len(temp_list)
# # print(temp_mean)
# print(data["temp"].mean())

# print(data["temp"].max())

# print(data["condition"])
# print(data.condition)

# max temp day
max_temp = data["temp"].max()
max_temp_day = data[data.temp == max_temp].day
print(max_temp_day)

monday = data[data.day == "Monday"]
print(f"F monday temp: {monday.temp * 1.8 + 32}")

# create a dataframe from scratch
data_dict = {
    "students": ["Amy", "James", "Angela"],
    "scores": [76, 56, 65]
}

data = pd.DataFrame(data_dict)
print(data)

data.to_csv("new_data.csv")