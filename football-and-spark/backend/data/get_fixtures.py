import http.client
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
API_KEY = os.getenv('API_KEY')

conn = http.client.HTTPSConnection("v3.football.api-sports.io")
headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': API_KEY
}

def get_fixtures(date):
    conn.request("GET", f"/fixtures?date={date}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    fixtures = json.loads(data.decode("utf-8"))
    # Save to json_data folder
    output_dir = os.path.join(os.path.dirname(__file__), "json_data")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"fixtures_{date}.json")
    with open(output_path, "w") as f:
        json.dump(fixtures, f, indent=2)
    print(f"Saved fixtures to {output_path}")
    return fixtures

if __name__ == "__main__":
    # HAS TO BE A DATE IN 2021 LETS DO THE FIRST FIXTURE 
    date = '2021-08-14'
    get_fixtures(date)
