import requests
from datetime import datetime

# load_dotenv will be used to load the .env file to the environment variables.
from dotenv import load_dotenv
# os will be used to refer to those variables in the code
import os

# Credentials
load_dotenv(".env")  # This will load the .env file


NUTRIONIX_APP_ID = os.getenv("NUTRIONIX_APP_ID")
NUTRIONIX_API_KEY = os.getenv("NUTRIONIX_API_KEY")

EXERCISE_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
REQUEST_HEADERS = {
    "x-app-id": NUTRIONIX_APP_ID,
    "x-app-key": NUTRIONIX_API_KEY,
    "Content-Type": "application/json"
}

exercise_input = input("Tell which exercise you did today?: ")

GENDER = "MALE"
WEIGHT_KG = "78"
HEIGHT_CM = "176"
AGE = "42"

params = {
     "query": exercise_input,
     "gender": GENDER,
     "weight_kg": WEIGHT_KG,
     "height_cm": HEIGHT_CM,
     "age": AGE,
}

response = requests.post(url=EXERCISE_ENDPOINT, json=params, headers=REQUEST_HEADERS)
response.raise_for_status()
result = response.json()

now = datetime.now()
today_date = now.strftime("%d/%m/%Y")
now_time = now.strftime("%H:%M")

sheety_endpoint = os.getenv("SHEETY_ENDPOINT")

for exercise in result["exercises"]:
    xrcise = exercise["name"].title()
    duration = exercise["duration_min"]
    calories = exercise["nf_calories"]

    new_record = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": xrcise,
            "duration": duration,
            "calories": calories
        }
    }

    sheety_request_headers = {
        "Content-Type": "application/json",
    }

    sheety_response = requests.post(url=sheety_endpoint, json=new_record, headers=sheety_request_headers)
    response.raise_for_status()
    print(sheety_response.text)

