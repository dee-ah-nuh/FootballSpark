import http.client
import json
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
API_KEY = os.getenv('API_KEY')

conn = http.client.HTTPSConnection("v3.football.api-sports.io")
headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': API_KEY
}

def get_predictions(fixture_id):
    conn.request("GET", f"/predictions?fixture={fixture_id}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    predictions = json.loads(data.decode("utf-8"))
    output_dir = os.path.join(os.path.dirname(__file__), "json_data")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"predictions_{fixture_id}.json")
    with open(output_path, "w") as f:
        json.dump(predictions, f, indent=2)
    print(f"Saved predictions to {output_path}")
    return predictions

if __name__ == "__main__":
    fixture_id = 12345  # Replace with actual fixture ID
    get_predictions(fixture_id)
