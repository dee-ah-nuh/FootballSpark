import http.client
import json
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
API_KEY = os.getenv('API_KEY')

if not API_KEY:
    raise ValueError("API_KEY not found. Please check your .env file and environment setup.")

# Demo: Call the API once for a single team, league, and season
LEAGUE_ID = 39  # Premier League
TEAM_ID = 33    # Example team ID
SEASON = 2021

conn = http.client.HTTPSConnection("v3.football.api-sports.io")
headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': API_KEY
}

print(f"Fetching statistics for team {TEAM_ID} in league {LEAGUE_ID}, season {SEASON}")
conn.request("GET", f"/teams/statistics?season={SEASON}&team={TEAM_ID}&league={LEAGUE_ID}", headers=headers)
res = conn.getresponse()
stats_data = res.read()
try:
    stats_response = json.loads(stats_data.decode("utf-8"))
except Exception as e:
    stats_response = {"error": str(e)}

output_dir = os.path.join(os.path.dirname(__file__), "json_data")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, f"team_statistics_{LEAGUE_ID}_{TEAM_ID}_{SEASON}.json")
with open(output_path, "w") as f:
    json.dump(stats_response, f, indent=2)

print(f"Saved demo team statistics to {output_path}")
print(json.dumps(stats_response, indent=2))
