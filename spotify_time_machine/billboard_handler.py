from datetime import timedelta, date
from bs4 import BeautifulSoup
import requests

# from main import get_saturday_of_week

"""
This class is responsible for getting the song titles from Billboard's Top 100 list
"""
class BillboardHandler():
    def __init__(self):
        self.titles = []
        self.BILLBOARD_BASE_URL = "https://www.billboard.com/charts/hot-100/"

    def get_saturday_of_week(self, input_date):
        """
        Calculates the date of the Saturday within the same week as the input_date.

        Args:
            input_date (str): The date for which to find the containing Saturday.
                in the format YYYY-MM-DD

        Returns:
            date: Saturday's date for the week containing input_date.
        """
        date_parts = input_date.split('-')
        user_date = date(year=int(date_parts[0]), month=int(date_parts[1]), day=int(date_parts[2]))

        day_of_week = user_date.isoweekday()
        saturday_date = user_date
        if day_of_week == 7:
            # Sunday - Saturday for the week is 6 days ahead
            saturday_date = user_date + timedelta(days=6)
        else:
            # Monday - Friday
            offset = 6 - day_of_week
            saturday_date = user_date + timedelta(days=offset)

        return saturday_date

    def get_songs_for_week(self, date):
        """
        gets the song titles from Billboard's Top 100 site for the specified date.
        :param date (str): string containing the day in the week to get the song titles from
        :return: a dictionary containing the song titles as keys and the artist as the value
        """
        week_date = self.get_saturday_of_week(date)

        # get page markup from Billboard
        response = requests.get(f"{self.BILLBOARD_BASE_URL}{week_date}/")
        page_data = response.text

        # scrap the page markup for the song titles
        soup = BeautifulSoup(markup=page_data, features='html.parser')
        title_tags = soup.select('div.o-chart-results-list-row-container h3.c-title.a-font-primary-bold-s')
        artist_tags = soup.select('div.o-chart-results-list-row-container h3.c-title.a-font-primary-bold-s + span.c-label')


        # build a list of song titles from the list of tags
        titles = [title.string.replace('\n', '').replace('\t', '') for title in title_tags]
        artists = [artist.string.replace('\n', '').replace('\t', '') for artist in artist_tags]

        # return dictionary with the title as the key and the artist as the value
        return dict(zip(titles, artists))