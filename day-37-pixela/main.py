import requests
import dotenv
import os
from datetime import datetime

dotenv.load_dotenv()

TOKEN = os.getenv("TOKEN")
USERNAME = os.getenv("USERNAME")
GRAPH_ID = "graph1"

# STEP 1: Create a user
def create_user():
    user_parameters = {
        "token": TOKEN,
        "username": USERNAME,
        "agreeTermsOfService": "yes",
        "notMinor": "yes"
    }

    response = requests.post(url="https://pixe.la/v1/users", json=user_parameters)
    response.raise_for_status()

# STEP 2: Create a graph
def create_graph():
    graph_parameters = {
        "id": "graph1",
        "name": "100 days of code",
        "unit": "commit",
        "type": "int",
        "color": "ajisai",
        "timezone": "Asia/Tokyo"
    }

    headers = {
        "X-USER-TOKEN": TOKEN
    }

    CREATION_ENDPOINT = f"https://pixe.la/v1/users/{USERNAME}/graphs"

    response = requests.post(url=CREATION_ENDPOINT, json=graph_parameters, headers=headers)
    response.raise_for_status()

# STEP 3: Create a pixel
def create_pixel(date: str, quantity: str, optional_data: str):
    pixel_parameters = {
        "date": date,
        "quantity": quantity,
        "optionalData": optional_data
    }

    headers = {
        "X-USER-TOKEN": TOKEN
    }

    PIXEL_ENDPOINT = f"https://pixe.la/v1/users/{USERNAME}/graphs/{GRAPH_ID}"

    response = requests.post(url=PIXEL_ENDPOINT, json=pixel_parameters, headers=headers)
    response.raise_for_status()

# create_pixel(date=datetime.now().strftime("%Y%m%d"), 
#              quantity="10", 
#              optional_data='{"day": "37","language": "Python","content": "pixela"}')

# STEP 4: Update a pixel
def update_pixel(date: str, quantity: str):
    pixel_parameters = {
        "quantity": quantity
    }

    headers = {
        "X-USER-TOKEN": TOKEN
    }
    
    PIXEL_ENDPOINT = f"https://pixe.la/v1/users/{USERNAME}/graphs/{GRAPH_ID}/{date}"

    response = requests.put(url=PIXEL_ENDPOINT, json=pixel_parameters, headers=headers)
    response.raise_for_status()

# update_pixel(date=datetime.now().strftime("%Y%m%d"), 
#              quantity="1")

# STEP 5: Delete a pixel
def delete_pixel(date: str):
    PIXEL_ENDPOINT = f"https://pixe.la/v1/users/{USERNAME}/graphs/{GRAPH_ID}/{date}"

    response = requests.delete(url=PIXEL_ENDPOINT, headers={"X-USER-TOKEN": TOKEN})
    response.raise_for_status()

# delete_pixel(date=datetime.now().strftime("%Y%m%d"))

# STEP 6: Get latest pixel
def get_latest_pixel():
    PIXEL_ENDPOINT = f"https://pixe.la/v1/users/{USERNAME}/graphs/{GRAPH_ID}/latest"

    response = requests.get(url=PIXEL_ENDPOINT, headers={"X-USER-TOKEN": TOKEN})
    response.raise_for_status()

    return response.json()

print(get_latest_pixel())