import requests
from bs4 import BeautifulSoup

import os
import json
from dotenv import load_dotenv, find_dotenv

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load 100 song names form Billboard.com -------------------------------------------------------------------------------

def request_tracks():
    """
    Requests the 100 top tracks for the given year and month in the parameters form https://www.billboard.com/charts/hot-100.
    :return: The request response text
    """
    year_month = input("Please select the date of the music you would like to hear in format YYYY-MM: ")

    try:
        with open(f"{year_month}-track-response.txt", mode="r", encoding="utf-8") as file:
            response_text = file.read()
    except OSError:
        request_url = f"https://www.billboard.com/charts/hot-100/{year_month}-01/"
        header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}
        response = requests.get(url=request_url, headers=header)
        response_text = response.text

        with open(f"{year_month}-track-response.txt", mode="w", encoding="utf-8") as file:
            file.write(response.text)

    name = f"{year_month} Billboard Top 100"

    return response_text, name


def parse_request(text):
    """
    Uses BeautifulSoup to parse the requested html text and obtain the correct artist and track lists
    :param text: Requested response text
    :return:
        track_list (list): List containing the names of all the tracks
        artist_list (list): List containing the names of all artists
    """
    soup = BeautifulSoup(text, "html.parser")
    html_track_list = soup.select(selector="div ul li ul li h3")
    html_artist_list = soup.select(selector="div ul li ul li span")[::7]    # Jumps seven items to get the correct artist content

    track_list = [html_track.getText().strip() for html_track in html_track_list]
    artist_list = [html_artist.getText().strip() for html_artist in html_artist_list]

    return track_list, artist_list


def spotify_login(scope: str, client_id: str, client_secret: str, redirect_uri: str):
    """
    Returns a spotipy login object based on a specific scope function implemented by spotify API.
    :param scope: Defines th typo of action to do.
                    Read more here https://developer.spotify.com/documentation/web-api/concepts/scopes
    :return: access_token (str): Access token to make API calls
             user_id (str): User id for the API calls
    """

    client = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

    access_token = os.getenv("SPOTIFY_ACCESS_TOKEN")
    user_id = client.me()["id"]

    return client, access_token, user_id


def create_playlist(client: spotipy, user_id: int, playlist_name: str):
    """
    Creates a new playlist in spotify.
    :param client: Client spotipy login
    :param user_id: Spotify user id
    :param playlist_name: Name of the playlist
    :return: Returns the playlist id
    """
    playlists = client.user_playlists(user=user_id)

    for p in playlists["items"]:
        if p["name"] == playlist_name:
            return p["id"]

        else:
            playlist = client.user_playlist_create(user=user_id, name=playlist_name, public=True)
            return playlist["id"]



def find_track_uris(client: spotipy, track_list: list, artist_list: list):
    """
    Finds the unique uri's of the tracks to add to the playlist and puts them in a list.
    :param client: Client spotipy login
    :param track_list: List of tracks to append
    :param artist_list: List of the corresponding artists in order of track list
    :return: Returns the track uri's in a list
    """
    track_uris = []
    for track, artist in zip(track_list, artist_list):
        search = client.search(q=f"track: {track}, artist: {artist}")["tracks"]["items"][0]
        track_uris.append(search["uri"])

    return track_uris



if __name__ == "__main__":

    load_dotenv(find_dotenv())

    CLIENT_ID = os.getenv("SPOTIFY_ID")
    CLIENT_SECRET = os.getenv("SPOTIFY_SECRET")
    REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

    response_text, playlist_name = request_tracks()
    track_list, artist_list = parse_request(response_text)
    sp, access_token, user_id = spotify_login("playlist-modify-public", CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    playlist_id = create_playlist(sp, user_id, playlist_name)
    track_uris = find_track_uris(sp, track_list, artist_list)
    sp.playlist_add_items(playlist_id=playlist_id, items=track_uris)
