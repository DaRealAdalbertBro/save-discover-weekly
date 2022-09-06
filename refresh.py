import requests
import json


import os
from dotenv import load_dotenv
load_dotenv()

refresh_token = os.getenv('TOKEN')
base_64 = os.getenv('base_64')

class Refresh:

    def __init__(self):
        self.refresh_token = refresh_token
        self.base_64 = base_64

    def refresh(self):

        query = "https://accounts.spotify.com/api/token"

        response = requests.post(query,
                                 data={"grant_type": "refresh_token",
                                       "refresh_token": refresh_token},
                                 headers={"Authorization": "Basic " + base_64})

        response_json = response.json()
        print(response_json)

        return response_json["access_token"]


a = Refresh()
a.refresh()