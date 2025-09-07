import requests
import json
from datetime import datetime

API_KEY = "1c4235d512452af307933a9088a514d9"
BASE_URL = "https://v3.football.api-sports.io"

# Top 15 European leagues (add more IDs as needed)
TOP_EUROPE_LEAGUE_IDS = [39, 140, 135, 78, 61, 88, 94, 2, 3, 4, 5, 6, 7, 8, 9]
# Top 5 world competitions (Champions League, Europa League, World Cup, etc.)
TOP_WORLD_COMPETITION_IDS = [2, 3, 4, 5, 1]  # Example IDs, update as needed

HEADERS = {"x-apisports-key": API_KEY}


def get_matches_for_leagues(league_ids, season=None):
    all_matches = {}
    for league_id in league_ids:
        params = {"league": league_id}
        if season:
            params["season"] = season
        url = f"{BASE_URL}/fixtures"
        response = requests.get(url, headers=HEADERS, params=params)
        if response.status_code == 200:
            data = response.json()
            all_matches[league_id] = data.get("response", [])
        else:
            print(f"Error fetching league {league_id}: {response.status_code}")
            all_matches[league_id] = []
    return all_matches


def save_matches_to_json(matches, filename):
    with open(filename, "w") as f:
        json.dump(matches, f, indent=2)


def main():
    season = datetime.now().year
    europe_matches = get_matches_for_leagues(TOP_EUROPE_LEAGUE_IDS, season)
    world_matches = get_matches_for_leagues(TOP_WORLD_COMPETITION_IDS, season)
    all_matches = {
        "europe": europe_matches,
        "world": world_matches
    }
    save_matches_to_json(all_matches, "top_leagues_matches.json")
    print("Saved match info to top_leagues_matches.json")

if __name__ == "__main__":
    main()
