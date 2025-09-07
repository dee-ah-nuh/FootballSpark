import http.client
import json
import os
from dotenv import load_dotenv

def fetch_players_for_team(api_key, team_id, season, output_json_path):
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': api_key
    }
    print(f"Calling API for players in team {team_id}, season {season}")
    conn.request("GET", f"/players?team={team_id}&season={season}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    players_response = json.loads(data.decode("utf-8"))
    players = players_response.get('response', [])
    with open(output_json_path, "w") as f:
        json.dump(players, f, indent=2)
    print(f"Saved {len(players)} players to {output_json_path}")

if __name__ == "__main__":
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY not found. Please check your .env file and environment setup.")
    # Example usage: fetch players for team 33 in season 2021
    team_id = 33  # Update with your actual team ID
    season = 2021
    output_json_path = f"json_data/players_{season}_team_{team_id}.json"
    fetch_players_for_team(api_key, team_id, season, output_json_path)
