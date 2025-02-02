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
print(popular_games[:10])
