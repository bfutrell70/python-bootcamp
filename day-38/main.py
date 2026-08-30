import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

SHEETY_URL = "https://api.sheety.co/a7c1bf7011705884125c54538c053929/myWorkouts/workouts"

BASE_URL = "https://trackapi.nutritionix.com"
ENDPOINT = "/v2/natural/exercise"
APP_ID = os.environ["APP_ID"]
APP_KEY = os.environ["API_KEY"]
API_URL = f"{BASE_URL}{ENDPOINT}"
# print(API_URL)


def get_exercise():
    """

    :return: a dictionary containing the values to add to the Google Sheet
    """
    exercises = input("Tell me which exercises you did: ")

    headers = {
        "x-app-id": APP_ID,
        "x-app-key": APP_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "query": exercises,
        "gender": "male",
        "age": 55
    }

    result = requests.post(url=API_URL, headers=headers, json=data).json()

    now = datetime.now()
    rows = []

    for exercise in result["exercises"]:
        rows.append({
            "date": now.date().strftime("%d/%m/%Y"),
            "time": now.time().strftime("%H:%M:%S"),
            "exercise": exercise["name"],
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        })

    return rows

def add_row_to_sheet(data):
    header = {
        "Authorization": "Bearer ufoireajglkvaliu4r9q84305toirestre"
    }

    for row in data:
        workout = {
            "workout": {
                "date": row["date"],
                "time": row["time"],
                "exercise": row["exercise"],
                "duration": row["duration"],
                "calories": row["calories"]
            }
        }

        result = requests.post(SHEETY_URL, headers=header, json=workout)

        print(result.text)


# ----- main program execution -----
exercise_data = get_exercise()
print(exercise_data)
add_row_to_sheet(exercise_data)
