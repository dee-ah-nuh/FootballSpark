import http.client
import json

API_KEY = "1c4235d512452af307933a9088a514d9"

# Example: Get statistics for a team in a league and season
TEAM_ID = 33  # Example team
LEAGUE_ID = 39  # Premier League
SEASON = 2024

conn = http.client.HTTPSConnection("v3.football.api-sports.io")
headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': API_KEY
}
conn.request("GET", f"/teams/statistics?season={SEASON}&team={TEAM_ID}&league={LEAGUE_ID}", headers=headers)
res = conn.getresponse()
data = res.read()
statistics = json.loads(data.decode("utf-8"))

with open("team_statistics_response.json", "w") as f:
    json.dump(statistics, f, indent=2)

print("Saved team statistics to team_statistics_response.json")
