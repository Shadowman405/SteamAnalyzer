import requests
import json
import datetime
import os
import pandas as pd

with open('D:/steam.txt', 'r') as file:
    steam_key = file.readline().strip()

API_KEY = steam_key
URL = f"https://api.steampowered.com/ISteamChartsService/GetMostPlayedGames/v1/?key={API_KEY}"
current_datetime = datetime.datetime.now()
year = current_datetime.year
month = current_datetime.month
day = current_datetime.day
response = requests.get(URL, timeout=30)
filename = f'popular_steam_games_{year}{month}{day}'

# Method for API call for top-100 steam games
if response.status_code == 200:
    def get_popular_games():
        popular_games_data = response.json()
        data = popular_games_data['response']['ranks']

        with open(f'{filename}.json', 'w') as file:
            json.dump(data, file, indent=4)

        #return popular_games_data
        #return data['response']['ranks']

# Call
get_popular_games()

# Read JSON file
with open(f'{filename}.json', 'r') as f:
    data = json.load(f)

# Convert JSON to DataFrame
df = pd.json_normalize(data)

# Create CSV file
df.to_csv(f'{filename}.csv', index=False)

# Delete JSON file
os.remove(f'{filename}.json')
