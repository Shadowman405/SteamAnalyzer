import requests
import json
import time
import os
import pandas as pd
from GetPopularGames import get_popular_games
from sqlalchemy import create_engine, Column, Integer, DateTime, String, Boolean, ARRAY, VARCHAR
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker

# №2 DAG
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
                current_players_and_appid = {'appid': app_id, 'current_players': data['response']['player_count']}
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

with open('steam_current_players_for_game.json', 'w', encoding='utf-8') as f:
    json.dump(current_players, f, ensure_ascii=False, indent=4)

# DATABASE PART
with open('D:/database.txt', 'r') as file:
    database = file.readline().strip()

engine = create_engine(f'{database}')

Base = declarative_base()

# Create the table in the database
Base.metadata.create_all(engine)

# Read JSON file
with open('steam_current_players_for_game.json', 'r') as f:
    data = json.load(f)

# Convert JSON to DataFrame
df = pd.json_normalize(data)

# Create CSV file
df.to_csv('steam_current_players_for_game.csv', index=False)


# Delete JSON file
os.remove('steam_current_players_for_game.json')


class CurrentPlayersForGame(Base):
    __tablename__ = 'top_steam_players_count_for_game'

    req_id = Column(String, nullable=False, unique=True, primary_key=True, autoincrement=True)
    appid = Column(Integer, nullable=True)
    current_players = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()

    df = pd.read_csv('steam_current_players_for_game.csv')

    # Insert data into the table
    df.to_sql('top_steam_players_count_for_game', engine, if_exists='append', index=False)

    print(f"Loaded data from top_steam_games_details.csv")

    # Commit the session
    session.commit()

    # Close the session
    session.close()

    # Deleting csv file
    os.remove('steam_current_players_for_game.csv')
