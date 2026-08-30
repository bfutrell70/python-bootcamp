"""
This file handles interfacing with Spotify's API.
- request an access token
    - returns access_token, token_type, expires_in
- create a playlist
    - playlist
        - options are public or private
- find a song URI
    - may not necessarily get a result
"""
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import time


class SpotifyHandler:
    def __init__(self):
        load_dotenv()
        self.SPOTIPY_CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
        self.SPOTIPY_CLIENT_SECRET = os.environ["SPOTIPY_CLIENT_SECRET"]
        self.SPOTIPY_CALLBACK_URL = os.environ["SPOTIPY_CALLBACK_URL"]
        self.user_id = ""
        self.track_uris = []
        self.spotify = None
        self.year = ""
        self.playlists = []

        self.authenticate()

    def authenticate(self):
        """
        authenticate against Spotify's API, get the user ID
        :return:
        """
        scope = "playlist-modify-private"

        self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
            scope=scope,
            client_id=self.SPOTIPY_CLIENT_ID,
            client_secret=self.SPOTIPY_CLIENT_SECRET,
            redirect_uri=self.SPOTIPY_CALLBACK_URL)
        )

        self.user_id = self.spotify.current_user()["id"]

    def find_playlists(self, playlist_name):
        """
        find existing playlists with the same name that are owned by
        the currently logged in user's ID
        :param playlist_name: name of the playlist
        :return:
        """
        query = f"{playlist_name}"
        playlist_info = self.spotify.search(q=query, type="playlist", limit=10)

        self.playlists = []

        for playlist in playlist_info["playlists"]["items"]:
            if playlist["name"] == playlist_name and playlist["owner"]["id"] == self.user_id:
                self.playlists.append(playlist["uri"])

    def remove_existing_playlists(self, playlist_name):
        """
        remove existing playlists from the authenticated user matching playlist_name
        :param playlist_name: name of the playlist to find
        :return:  Nothing
        """
        # check if Spotify playlists with the same name and owned by me exist
        # if so unfollow them to remove them
        self.find_playlists(playlist_name=playlist_name)
        if len(self.playlists) > 0:
            for playlist in self.playlists:
                self.spotify.current_user_unfollow_playlist(playlist)


    def find_song_uri(self, song_title, artist, year):
        """
        search Spotify for a song/track based on the song title and year of release
        :param song_title: song title to search for
        :param artist: artist that performed the song
        :param year: year the song was released
        :return: URI of the song, or None if it wasn't found
        """
        query = f"track: {song_title}, year: {year}, artist: {artist}"

        result_limit = 10

        song_info = self.spotify.search(q=query, type="track", limit=result_limit)
        if "tracks" in song_info and  "items" in song_info["tracks"] and len(song_info["tracks"]["items"]) > 0:
            for entry in song_info['tracks']['items']:
                if song_title in entry['name'] and artist == entry['album']['artists'][0]['name']:
                    return entry["uri"]
        else:
            return None

    def build_song_uri_list(self, song_titles):
        """
        build a list of track URIs
        :param song_titles: a dictionary with song titles as keys and the artists as values
        :return: Nothing
        """
        titles = song_titles.keys()

        for title in titles:
            time.sleep(0.1)
            song_uri = self.find_song_uri(title, song_titles[title], self.year)
            if song_uri is not None:
                self.track_uris.append(song_uri)

    def create_playlist(self, week, song_titles):
        """
        Create a Spotify playlist with song titles
        :param week : week the song titles are for
        :param song_titles : a dictionary containing the song titles as keys and the artist as the value
        :return:
        """

        self.year = week.split("-")[0]

        self.build_song_uri_list(song_titles)

        # create a playlist
        # should ideally check to see if a playlist with the same name exists, and either remove it or
        #   clear the tracks from it to prevent duplicates
        # can use search() to see if a playlist exists
        # can use playlist_replace_items() to replace the playlist items with new ones
        # to remove a playlist use current_user_unfollow_playlist()
        playlist_name = f"{week} Billboard 100"

        self.remove_existing_playlists(playlist_name=playlist_name)

        print("Create Spotify Playlist")
        result = self.spotify.user_playlist_create(user=self.user_id, name=playlist_name, public=False)

        # add tracks to the playlist
        self.spotify.playlist_add_items(result["id"], self.track_uris)
