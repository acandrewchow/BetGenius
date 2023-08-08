import numpy as np
import pandas as pd
import json
import os
import requests
import sys
from dotenv import load_dotenv

import league_dictionary

load_dotenv()

API_KEY = os.environ.get('API_KEY_ANDREW')

bet_id = 0
sports_set = set()
leagues_set = set()

sports_leagues = requests.get(f'https://api.the-odds-api.com/v4/sports?apiKey={API_KEY}').json()

for league in sports_leagues:
    if league['has_outrights'] == False:
      sports_set.add(league["group"])
      leagues_set.add(league["title"])
      
sports = list(sports_set)
league = list(leagues_set)
sports_to_league = {}

for sport in sports:
  sports_to_league[sport] = []

for league in sports_leagues:
    if league['has_outrights'] == False:
      sports_to_league[league['group']].append(league['title'])

sports.remove("Soccer")
del sports_to_league["Soccer"]

def generate_user_data(records):
    user_ids = np.arange(1, records + 1)
    bet_ids = [str(i) for i in range(1, records + 1)]

    # Creates a data frame to illustrate user-to-bet association
    # User X placed Bet Y
    data = pd.DataFrame({
        'User': np.random.choice(user_ids, size=records, replace=True),
        'Bet': np.random.choice(bet_ids, size=records, replace=True)
    })

    return data

# saves a data frame to a CSV
def save_data_to_csv(data, file_path):
    data.to_csv(file_path, index=False)

def generate_bet_attributes(records):
    odds_values = np.random.uniform(low=-500, high=500, size=records)
    outcome_values = np.random.choice(['W', 'L'], size=records, replace=True)
    type_values = np.full(records, 'Straight')

    # generate sport values
    random_sports = np.random.choice(sports, size=records, replace=True)

    # generate league values
    league_values = np.array([np.random.choice(sports_to_league[sport]) for sport in random_sports])

    # generate team values
    team_values = np.array([np.random.choice(league_dictionary.league_to_team[league]) for league in league_values])

    # create data frame
    bet_attributes = pd.DataFrame({
        'Bet': [i+1 for i in range(records)],
        'Odds': odds_values,
        'Outcome': outcome_values,
        'Type': type_values,
        'Sport': random_sports,
        'League': league_values,
        'Team': team_values,
        'Market_Type': "h2h"
    })

    bet_attributes['Odds'] = bet_attributes['Odds'].apply(lambda x: '{:.0f}'.format(x))

    return bet_attributes

if __name__ == "__main__":

    records = int(sys.argv[1])

    # Generate data
    user_data = generate_user_data(records)
    bet_attributes_data = generate_bet_attributes(records)

    save_data_to_csv(user_data, "users.csv")
    save_data_to_csv(bet_attributes_data, "bet_attributes.csv")


