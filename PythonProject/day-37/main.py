import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# profile page: https://pixe.la/@bfutrell70

load_dotenv()

TOKEN = os.environ["TOKEN"]
USERNAME = "bfutrell70"
PIXELA_ENDPOINT = "https://pixe.la/v1/users"
GRAPH_NAME = "exercise1"

def create_user(username, token):
    """
    creates a user on Pixela
    :return:
    """
    params = {
        "token": token,
        "username": username,
        "agreeTermsOfService": "yes",
        "notMinor": "yes"
    }

    # post uses json instead of params
    response = requests.post(url=PIXELA_ENDPOINT, json=params)
    print(response.text)

def create_graph_definition(username, token, id):
    """
    create a graph on Pixela
    :param username: user account to add the graph to
    :param token: token used at the time the user was created
    :param id: id of the graph
    :return:
    """
    graph_endpoint = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs"
    graph_params = {
        "id": id,
        "name": "Exercise Graph",
        "unit": "minutes",
        "type": "float",
        "color": "shibafu",
        "timezone": "America/New_York"
    }

    # token must be sent in the header
    headers = {
        "X-USER-TOKEN": token
    }

    response = requests.post(url=graph_endpoint, headers=headers, json=graph_params)
    print(response)

def add_pixel_to_graph(username, token, graph_id, date, quantity):
    """
    add a data point to the graph
    :param username: user account that owns the graph
    :param graph_id: ID of the graph to add the data point to
    :param token: token used at the time the user account was made
    :param date: date to add the data point to
    :param quantity: value to assign to the data point
    :return:
    """
    add_pixel_endpoint = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs/{graph_id}"
    print(add_pixel_endpoint)

    params = {
        "date": date,
        "quantity": f"{quantity}"
    }

    # token must be sent in the header
    headers = {
        "X-USER-TOKEN": token
    }

    response = requests.post(url=add_pixel_endpoint, headers=headers, json=params)
    # printing just response only returns the HTTP status code.
    # printing the text property will display more information
    print(response.text)

def update_pixel(username, token, graph_id, date, quantity):
    """
    update an existing data point in the graph
    :param username: user account that owns the graph
    :param graph_id: ID of the graph to add the data point to
    :param token: token used at the time the user account was made
    :param date: date to add the data point to
    :param quantity: value to update the data point to
    :return:
    """
    update_pixel_endpoint = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs/{graph_id}/{date}"
    print(update_pixel_endpoint)

    params = {
        "quantity": f"{quantity}"
    }

    # token must be sent in the header
    headers = {
        "X-USER-TOKEN": token
    }

    response = requests.put(url=update_pixel_endpoint, headers=headers, json=params)
    # printing just response only returns the HTTP status code.
    # printing the text property will display more information
    print(response.text)

def delete_pixel(username, token, graph_id, date):
    """
    remove an existing data point in the graph
    :param username: user account that owns the graph
    :param graph_id: ID of the graph to remove the data point from
    :param token: token used at the time the user account was made
    :param date: date containing the data point to remove
    :return:
    """
    delete_pixel_endpoint = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs/{graph_id}/{date}"
    print(delete_pixel_endpoint)

    # token must be sent in the header
    headers = {
        "X-USER-TOKEN": token
    }

    response = requests.delete(url=delete_pixel_endpoint, headers=headers, json=None)
    # printing just response only returns the HTTP status code.
    # printing the text property will display more information
    print(response.text)

formatted_date = datetime.now().strftime("%Y%m%d")
yesterday = datetime(year=2025, month=5, day=26).strftime("%Y%m%d")

# create_user(USERNAME)
# create_graph_definition(USERNAME, TOKEN, GRAPH_NAME)
# add_pixel_to_graph(username=USERNAME, token=TOKEN, graph_id=GRAPH_NAME, date=yesterday, quantity=40)
# update_pixel(username=USERNAME, token=TOKEN, graph_id=GRAPH_NAME, date=yesterday, quantity=80)
delete_pixel(username=USERNAME, token=TOKEN, graph_id=GRAPH_NAME, date=yesterday)