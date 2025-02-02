import requests
import json
import time
from GetPopularGames import get_popular_games

with open('D:/steam.txt', 'r') as file:
    steam_key = file.readline().strip()

API_KEY = steam_key

popular_games_filename = get_popular_games()
print(popular_games_filename)

# JSON read
with open(f'{popular_games_filename}', 'r') as file:
    data = json.load(file)

# Extract appid
appid_list = [item['appid'] for item in data]
print(appid_list)
current_players = []


def get_current_players(app_id, max_retries=5, delay=10):
    url = f"https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={app_id}"
    retries = 0

    while retries < max_retries:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                current_players_and_appid = {'appid': {app_id}, 'current_players':{data['response']['player_count']}}
                print(current_players_and_appid)
                return current_players_and_appid
            else:
                print(f"Failed to get data for app_id {app_id}. Retrying in {delay} seconds...")
        except requests.RequestException as e:
            print(f"Request error: {e}. Retrying in {delay} seconds...")

        retries += 1
        time.sleep(delay)


for app_id in appid_list:
    players_data = get_current_players(app_id)
    if players_data:
        current_players.append(players_data)

print(current_players)
