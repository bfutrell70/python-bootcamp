from billboard_handler import BillboardHandler
from spotify_handler import SpotifyHandler
from dotenv import load_dotenv
import re

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0"
load_dotenv()

"""
This project gets the titles from the week specified by the user.
The titles are in <h3> tags with an ID of 'title-of-a-story', and a class of 'c-title'.
The ID 'title-of-a-story' should only appear once in the document, but appears in each title's <h3> tag.
"""

def get_date_from_user():
    """
    get a date from the user
    :return: a string containing a date in the format YYYY-MM-DD, or 'Q' to indicate
    """
    # request a date from the user, get Saturday's date containing the date
    # continue to prompt the user until a date in the specified format is entered, or the user types in "q"
    date_entered = None
    date_regex = r"\d{4}-\d{2}-\d{2}"
    exit_program = False
    user_date_string = ""
    while date_entered is None and exit_program == False:
        user_date_string = input(
            "Which year to you want to travel to? \nType the date in this format YYYY-MM-DD or 'q' to quit: \n")
        date_entered = re.search(date_regex, user_date_string)

        user_date_string = user_date_string.upper()

        if user_date_string == "Q":
            exit_program = True

    return user_date_string

user_date = get_date_from_user()

# user didn't quit
if user_date.upper() != "Q":
    # get song titles from Billboard's Top 100 list for the specified date
    billboard = BillboardHandler()
    titles = billboard.get_songs_for_week(user_date)

    if len(titles) > 0:
        # data is present, create the playlist
        spotify = SpotifyHandler()
        playlist = spotify.create_playlist(
            week=user_date,
            song_titles=titles
        )