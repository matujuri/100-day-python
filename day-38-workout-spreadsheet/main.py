import requests
import os
import dotenv

dotenv.load_dotenv()

EXERCISE_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"

headers = {
    "x-app-id": os.getenv("NUTRITIONIX_APP_ID"),
    "x-app-key": os.getenv("NUTRITIONIX_API_KEY")
}

body = {
    "query": input("Which exercise did you do today?")
}

response = requests.post(url=EXERCISE_ENDPOINT, headers=headers, json=body)
response.raise_for_status()

print(response.json())