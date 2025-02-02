import requests

with open('D:/steam.txt', 'r') as file:
    steam_key = file.readline().strip()

API_KEY = steam_key


def get_popular_games():
    url = f"https://api.steampowered.com/ISteamChartsService/GetMostPlayedGames/v1/?key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data['response']['ranks']


popular_games = get_popular_games()
top1_game_id = popular_games[1]['appid']

def get_game_details(app_id):
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    response = requests.get(url)
    data = response.json()
    return data[str(app_id)]['data']


top1_details = get_game_details(top1_game_id)
print(top1_details)


def get_current_players(app_id):
    url = f"https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={app_id}"
    response = requests.get(url)
    data = response.json()
    return data['response']['player_count']


top1_current_players = get_current_players(top1_game_id )
print(top1_current_players)
