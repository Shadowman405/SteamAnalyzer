import requests
import json
import datetime

with open('D:/steam.txt', 'r') as file:
    steam_key = file.readline().strip()

API_KEY = steam_key
URL = f"https://api.steampowered.com/ISteamChartsService/GetMostPlayedGames/v1/?key={API_KEY}"
current_datetime = datetime.datetime.now()
year = current_datetime.year
month = current_datetime.month
day = current_datetime.day
response = requests.get(URL, timeout=30)

if response.status_code == 200:
    def get_popular_games():
        popular_games_data = response.json()

        with open(f'popular_steam_games_{year}{month}{day}.json', 'w') as file:
            json.dump(popular_games_data, file, indent=4)

        return popular_games_data
        #return data['response']['ranks']


popular_games = get_popular_games()
