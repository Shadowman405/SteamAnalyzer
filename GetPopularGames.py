import requests

with open('D:/steam.txt', 'r') as file:
    steam_key = file.readline().strip()

API_KEY = steam_key


def get_popular_games():
    url = f"https://api.steampowered.com/ISteamChartsService/GetMostPlayedGames/v1/?key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data
    #return data['response']['ranks']


def get_game_details(app_id):
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    response = requests.get(url)
    data = response.json()
    return data[str(app_id)]['data']


def get_current_players(app_id):
    url = f"https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={app_id}"
    response = requests.get(url)
    data = response.json()
    return data['response']['player_count']


popular_games = get_popular_games()

for game in popular_games[:5]:
    app_id = game['appid']
    details = get_game_details(app_id)
    current_players = get_current_players(app_id)

