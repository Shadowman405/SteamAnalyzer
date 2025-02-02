import requests
import json
import datetime
import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

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

# DATABASE PART
with open('D:/database.txt', 'r') as file:
    database = file.readline().strip()

engine = create_engine(f'{database}')

Base = declarative_base()

# Create the table in the database
Base.metadata.create_all(engine)


class Weather(Base):
    __tablename__ = 'top_steam_games'

    req_id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    rank = Column(Integer, nullable=True)
    appid = Column(Integer, nullable=True)
    last_week_rank = Column(Integer, nullable=True)
    peak_in_game = Column(Integer, nullable=True)


# Create a session
Session = sessionmaker(bind=engine)
session = Session()

df = pd.read_csv(f'{filename}.csv')

# Insert data into the table
df.to_sql('top_steam_games', engine, if_exists='append', index=False)

print(f"Loaded data from {filename}.csv")

# Commit the session
session.commit()

# Close the session
session.close()

# Deleting csv file
os.remove(f'{filename}.csv')
print(f'{filename}.csv successfully deleted')
