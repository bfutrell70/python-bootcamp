import requests

BASE_URL = "https://opentdb.com/api.php"

def get_questions():
    """
    makes an API call to opentdb.com to get 10 true/false questions, assign to question_data
    :return:
    """
    global question_data
    parameters = {
        "amount": 10,
        "type": "boolean",
        "category": 18
    }

    response = requests.get(url=BASE_URL, params=parameters)
    response.raise_for_status()

    return response.json()["results"]

question_data = get_questions()

