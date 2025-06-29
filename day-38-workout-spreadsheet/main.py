import requests
import os
import dotenv
from workout import Workout
from typing import List

dotenv.load_dotenv()
SHEETY_ID = os.getenv("SHEETY_ID")
SHEETY_TOKEN = os.getenv("SHEETY_TOKEN")

EXERCISE_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
SHEETY_ENDPOINT = f"https://api.sheety.co/{SHEETY_ID}/workoutTracking/workouts"

def get_workout_data(exercise: str) -> list:
    headers = {
        "x-app-id": os.getenv("NUTRITIONIX_APP_ID"),
        "x-app-key": os.getenv("NUTRITIONIX_API_KEY")
    }
    body = {
        "query": exercise
    }

    response = requests.post(url=EXERCISE_ENDPOINT, headers=headers, json=body)
    response.raise_for_status()
    return response.json()["exercises"]

def get_workout_list(exercise: str) -> List[Workout]:
    workout_data = get_workout_data(exercise)
    return [Workout(
        exercise=workout["name"].title(),
        duration=workout["duration_min"],
        calories=workout["nf_calories"]
    ) for workout in workout_data]
    
def add_workout_to_spreadsheet(workout_list: List[Workout]):
    for workout in workout_list:
        response = requests.post(url=SHEETY_ENDPOINT, json={"workout": workout.to_dict()}, headers={"Authorization": f"Bearer {SHEETY_TOKEN}"})
        response.raise_for_status()
        print(response.json())

exercise = input("Which exercise did you do today?")
workout_list = get_workout_list(exercise)
add_workout_to_spreadsheet(workout_list)