import http.client
import json
import os
from datetime import datetime, time
from dotenv import load_dotenv


def fetch_teams_and_players(api_key, league_ids, season):
    """
    Fetches all teams and their players for the given league IDs and season.
    Returns a dictionary with league_id as keys and team+player info as values.
    """
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': api_key
    }

        # Limit to a single API call for demonstration
    LEAGUE_ID = 39  # Premier League
    SEASON = season

    print(f"Fetching teams for league {LEAGUE_ID}, season {SEASON}...")
    conn.request("GET", f"/teams?league={LEAGUE_ID}&season={SEASON}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    teams_response = json.loads(data.decode("utf-8"))
    teams = teams_response.get('response', [])

    # save teams
    for team in teams:
        team_id = team['team']['id']
        team_name = team['team']['name']
        print(f"Found team: {team_name} (ID: {team_id})")
        # Save team info
        result[LEAGUE_ID] = result.get(LEAGUE_ID, []) + [team]

    # Save to JSON
    with open(f"teams_response_{LEAGUE_ID}.json", "w") as f:
        json.dump(teams, f, indent=2)

    time.sleep(60)  # To respect API rate limits

    result = {}
    if teams:
        team_info = teams[0]
        team_id = team_info['team']['id']
        print(f"Fetching players for team {team_id} in league {LEAGUE_ID}, season {SEASON}...")
        conn.request("GET", f"/players?team={team_id}&season={SEASON}", headers=headers)
        res = conn.getresponse()
        players_data = res.read()
        players_response = json.loads(players_data.decode("utf-8"))
        team_info['players'] = players_response.get('response', [])
        result[LEAGUE_ID] = [team_info]
    else:
        result[LEAGUE_ID] = []

    return result



def main():
    # Load API key from .env file
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
    api_key = os.getenv('API_KEY')

    if not api_key:
        raise ValueError("API_KEY not found. Please check your .env file and environment setup.")

    # Example league IDs
    league_ids = [39, 140, 135, 78, 61, 88, 94, 253, 262, 307, 98, 292, 169, 323]
    season = 2021

    # Fetch data
    all_data = fetch_teams_and_players(api_key, league_ids, season)



if __name__ == "__main__":
    main()
