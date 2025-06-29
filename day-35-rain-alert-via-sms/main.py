import requests
import dotenv
import os
from message import Message
dotenv.load_dotenv()

OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.getenv("OWM_API_KEY")

message = Message()

parameters = {
    "lat": 35.467560,
    "lon": 139.625586,
    "appid": api_key,
    "cnt": 8
}

response = requests.get(OWM_ENDPOINT, params=parameters)
response.raise_for_status()

data = response.json()

weather_data = data["list"]
# 6時から21時までのデータを取得
for weather in weather_data[1:7]:
    if weather["weather"][0]["id"] < 700:
        print("Bring an umbrella")
        message.send_message(body="It's going to rain today. Remember to bring an umbrella.")
        break
else:
    print("No umbrella needed")









