# match_finder.py
"""
Extracts football/soccer match info for major leagues given a location and date.

Features:
- Nearby matches
- When/where
- Distance from user
- Ticket price estimates
- Expected attendance
- Popularity score
- Match importance

Leagues covered:
Europe: Premier League, La Liga, Serie A, Bundesliga, Ligue 1, Eredivisie, Primeira Liga
Americas: MLS, Liga MX
Asia: Saudi Pro League, J-League, K-League, Chinese Super League, Indian Super League, Thai League
"""

from typing import List, Dict, Any
from datetime import datetime
import requests

# Placeholder for actual API integration
LEAGUES = [
    "Premier League", "La Liga", "Serie A", "Bundesliga", "Ligue 1", "Eredivisie", "Primeira Liga",
    "MLS", "Liga MX",
    "Saudi Pro League", "J-League", "K-League", "Chinese Super League", "Indian Super League", "Thai League"
]

class MatchInfo:
    def __init__(self, league: str, teams: str, date: str, location: str, distance_km: float,
                 ticket_price: float, attendance: int, popularity: float, importance: str):
        self.league = league
        self.teams = teams
        self.date = date
        self.location = location
        self.distance_km = distance_km
        self.ticket_price = ticket_price
        self.attendance = attendance
        self.popularity = popularity
        self.importance = importance

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__


# API-Football v3 integration
API_KEY = "1c4235d512452af307933a9088a514d9"
BASE_URL = "https://v3.football.api-sports.io"

# Map league names to API-Football league IDs (partial, add more as needed)
LEAGUE_IDS = {
    "Premier League": 39,
    "La Liga": 140,
    "Serie A": 135,
    "Bundesliga": 78,
    "Ligue 1": 61,
    "Eredivisie": 88,
    "Primeira Liga": 94,
    "MLS": 253,
    "Liga MX": 262,
    "Saudi Pro League": 307,
    "J-League": 98,
    "K-League": 292,
    "Chinese Super League": 169,
    "Indian Super League": 323,
    "Thai League": 332
}

def fetch_matches_for_league(league: str, location: str, date: str) -> List[MatchInfo]:
    league_id = LEAGUE_IDS.get(league)
    if not league_id:
        return []
    headers = {
        "x-apisports-key": API_KEY
    }
    params = {
        "league": league_id,
        "season": datetime.strptime(date, "%Y-%m-%d").year,
        "date": date
    }
    url = f"{BASE_URL}/fixtures"
    response = requests.get(url, headers=headers, params=params)
    matches = []
    if response.status_code == 200:
        data = response.json()
        for item in data.get("response", []):
            fixture = item["fixture"]
            teams = item["teams"]
            venue = fixture.get("venue", {})
            # TODO: Calculate distance from user location using geocoding
            # TODO: Estimate ticket price, attendance, popularity, importance
            match = MatchInfo(
                league=league,
                teams=f"{teams['home']['name']} vs {teams['away']['name']}",
                date=fixture["date"],
                location=venue.get("name", "Unknown"),
                distance_km=0.0,  # Placeholder
                ticket_price=0.0,  # Placeholder
                attendance=0,      # Placeholder
                popularity=0.0,    # Placeholder
                importance=""      # Placeholder
            )
            matches.append(match)
    else:
        print(f"API error for {league}: {response.status_code}")
    return matches

def find_nearby_matches(location: str, date: str) -> List[Dict[str, Any]]:
    results = []
    for league in LEAGUES:
        matches = fetch_matches_for_league(league, location, date)
        for match in matches:
            results.append(match.to_dict())
    return results

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python match_finder.py <location> <date: YYYY-MM-DD>")
        sys.exit(1)
    location = sys.argv[1]
    date = sys.argv[2]
    matches = find_nearby_matches(location, date)
    for match in matches:
        print(match)
