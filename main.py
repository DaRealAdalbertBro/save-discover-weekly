import json
import requests
from datetime import date
from refresh import Refresh
import PySimpleGUI as sg


import os
from dotenv import load_dotenv
load_dotenv()

CLIENT_USER_ID = os.getenv('CLIENT_USER_ID')
CLIENT_DISCOVER_WEEKLY = os.getenv('CLIENT_DISCOVER_WEEKLY')

songs_saved = False

class SaveSongs:
    def __init__(self):
        self.user_id = CLIENT_USER_ID
        self.spotify_token = ""
        self.discover_weekly_id = CLIENT_DISCOVER_WEEKLY
        self.tracks = ""
        self.new_playlist_id = ""

    def find_songs(self):
        # Loop through playlist tracks, add them to list
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(CLIENT_DISCOVER_WEEKLY)
        response = requests.get(query, headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.spotify_token)})
        response_json = response.json()
        print("Find-songs response:", response)

        for t in response_json["items"]:
            self.tracks += (t["track"]["uri"] + ",")

        self.tracks = self.tracks[:-1]
        self.add_to_playlist()

    # Create a new playlist
    def create_playlist(self):
        today = date.today()
        todayFormatted = today.strftime("%d/%m/%Y")
        query = "https://api.spotify.com/v1/users/{}/playlists".format(CLIENT_USER_ID)

        request_body = json.dumps({
            "name": todayFormatted + " discover weekly", "description": "Discover weekly rescued once again from the brink of destruction by your friendly neighbourhood python script", "public": True
        })

        response = requests.post(query, data=request_body, headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.spotify_token)
        })

        response_json = response.json()
        return response_json["id"]

    # Create playlist and add songs
    def add_to_playlist(self):
        self.new_playlist_id = self.create_playlist()
        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(self.new_playlist_id, self.tracks)
        response = requests.post(query, headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.spotify_token)})
        print("Add-to-playlist response:", response.json)

    # Refresh token
    def call_refresh(self):
        refreshCaller = Refresh()
        self.spotify_token = refreshCaller.refresh()
        self.find_songs()

layout = [[sg.Text("Spotify - Save current discover weekly")], [sg.Button("SAVE")], [sg.Button("CLOSE")]]
window = sg.Window("Spotify - Save DW", layout)

# Create an event loop
while True:
    event, values = window.read()
    if songs_saved == False and (event == "SAVE" or event == sg.WIN_CLOSED):
        window['SAVE'].update(disabled=True)
        a = SaveSongs()
        a.call_refresh()
        songs_saved = True
    
    if event == "CLOSE" or event == sg.WIN_CLOSED:
        break

window.close()