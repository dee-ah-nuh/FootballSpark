import http.client
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load API key from .env
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
API_KEY = os.getenv('API_KEY')

# Top 15 European leagues
EUROPE_LEAGUE_IDS = [39, 140, 135, 78, 61, 88, 94, 2, 3, 4, 5, 6, 7, 8, 9]
# Top 10 Americas leagues (example IDs, update as needed)
AMERICAS_LEAGUE_IDS = [253, 262, 265, 266, 267, 268, 269, 270, 271, 272]
# Top 5 Asia leagues (example IDs, update as needed)
ASIA_LEAGUE_IDS = [307, 98, 292, 169, 323]

ALL_LEAGUE_IDS = EUROPE_LEAGUE_IDS + AMERICAS_LEAGUE_IDS + ASIA_LEAGUE_IDS
SEASON = datetime.now().year

conn = http.client.HTTPSConnection("v3.football.api-sports.io")
headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': API_KEY
}

all_teams = {}
for league_id in ALL_LEAGUE_IDS:
    print(f"Fetching teams for league {league_id}, season {SEASON}")
    conn.request("GET", f"/teams?league={league_id}&season={SEASON}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    teams_response = json.loads(data.decode("utf-8"))
    all_teams[league_id] = [team['team']['id'] for team in teams_response.get('response', [])]

with open("all_teams_ids.json", "w") as f:
    json.dump(all_teams, f, indent=2)

print("Saved all team IDs to all_teams_ids.json")
