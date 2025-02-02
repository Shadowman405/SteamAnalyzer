import requests
import json
import time
import datetime
import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, DateTime, String, Boolean, ARRAY, VARCHAR
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
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
games_with_details = []


def get_current_players(app_id, max_retries=5, delay=10):
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    retries = 0

    while retries < max_retries:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data[str(app_id)]['success']:
                    game_data = data[str(app_id)]['data']
                    selected_data = {
                        "type": game_data.get('type'),
                        "name": game_data.get('name'),
                        "steam_appid": game_data.get('steam_appid'),
                        "required_age": game_data.get('required_age'),
                        "is_free": game_data.get('is_free'),
                        "developers": game_data.get('developers'),
                        "publishers": game_data.get('publishers')
                    }
                    print(selected_data)
                    return selected_data
                else:
                    print(f"Failed to get data for app_id {app_id}. Retrying in {delay} seconds...")
            else:
                print(f"Request failed with status code {response.status_code}. Retrying in {delay} seconds...")
        except requests.RequestException as e:
            print(f"Request error: {e}. Retrying in {delay} seconds...")

        retries += 1
        time.sleep(delay)

    print(f"Failed to get data for app_id {app_id} after {max_retries} attempts")
    return None


games_with_details = []
for app_id in appid_list:
    game_data = get_current_players(app_id)
    if game_data:
        games_with_details.append(game_data)


with open('steam_games_details.json', 'w', encoding='utf-8') as f:
    json.dump(games_with_details, f, ensure_ascii=False, indent=4)




# DATABASE PART
with open('D:/database.txt', 'r') as file:
    database = file.readline().strip()

engine = create_engine(f'{database}')

Base = declarative_base()

# Create the table in the database
Base.metadata.create_all(engine)

# Read JSON file
with open('steam_games_details.json', 'r') as f:
    data = json.load(f)

# Convert JSON to DataFrame
df = pd.json_normalize(data)

# Create CSV file
df.to_csv('top_steam_games_details.csv', index=False)


# Delete JSON file
os.remove(f'{popular_games_filename}')
os.remove('steam_games_details.json')


class TopSteamGameDetails(Base):
    __tablename__ = 'top_steam_games_details'

    req_id = Column(String, nullable=False, unique=True, primary_key=True, autoincrement=True)
    type = Column(VARCHAR(256), nullable=True)
    name = Column(VARCHAR(256), nullable=True)
    steam_appid = Column(Integer, nullable=True)
    required_age = Column(Integer, nullable=True)
    is_free = Column(Boolean, nullable=True)
    developers = Column(VARCHAR(1024), nullable=True)
    publishers = Column(VARCHAR(1024), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()

    df = pd.read_csv('top_steam_games_details.csv')

    # Insert data into the table
    df.to_sql('top_steam_games_details', engine, if_exists='append', index=False)

    print(f"Loaded data from top_steam_games_details.csv")

    # Commit the session
    session.commit()

    # Close the session
    session.close()

    # Deleting csv file
    os.remove('top_steam_games_details.csv')
    print('top_steam_games_details.csv successfully deleted')
