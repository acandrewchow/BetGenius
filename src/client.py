import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get('API_KEY_ANDREW')

sports_leagues = requests.get(f'https://api.the-odds-api.com/v4/sports?apiKey={API_KEY}').json()
available_bets_dict = []

for league in sports_leagues:
    if league['has_outrights'] == False:
        available_bets = requests.get(f'https://api.the-odds-api.com/v4/sports/{league["key"]}/odds/?regions=us&oddsFormat=american&markets=h2h&apiKey={API_KEY}').json()
        for bet in available_bets:
            if bet['bookmakers'] != []:
                bet_home = {
                    "sport_key": bet['sport_key'],
                    "sport_title": bet['sport_title'],
                    "home_team": bet['home_team'],
                    "away_team": bet['away_team'],
                    "market_type": "h2h",
                    "winning_team": bet['bookmakers'][0]['markets'][0]['outcomes'][0]['name'],
                    "odds": bet['bookmakers'][0]['markets'][0]['outcomes'][0]['price']
                }
                bet_away = {
                    "sport_key": bet['sport_key'],
                    "sport_title": bet['sport_title'],
                    "home_team": bet['home_team'],
                    "away_team": bet['away_team'],
                    "market_type": "h2h",
                    "winning_team": bet['bookmakers'][0]['markets'][0]['outcomes'][1]['name'],
                    "odds": bet['bookmakers'][0]['markets'][0]['outcomes'][1]['price']
                }
                available_bets_dict.append(bet_away)
                available_bets_dict.append(bet_home)

print(json.dumps(available_bets_dict, indent=2))
