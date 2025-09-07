import http.client
import json 
import os 
import pandas as pd

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../database/utils'))

from sqlite_utils import insert_dataframe_to_table #type: ignore

conn = http.client.HTTPSConnection("v3.football.api-sports.io")

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "1c4235d512452af307933a9088a514d9"
    }

# conn.request("GET", "/leagues", headers=headers)

# res = conn.getresponse()
# data = res.read()


# output_dir = os.path.join(os.path.dirname(__file__), "json_data")
# os.makedirs(output_dir, exist_ok=True)
# output_path = os.path.join(output_dir, f"all_leagues.json")
# with open(output_path, "w") as f:
#     json.dump(json.loads(data.decode("utf-8")), f, indent=2)



def get_all_leagues_parser(json_path):
    """
    Loads the API-Football leagues JSON and returns:
      - leagues_df: one row per league
      - league_seasons_df: one row per (league_id, season_year) with flattened coverage flags
    """
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"File not found: {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Normalize seasons as records; carry league/country as metadata
    seasons_flat = pd.json_normalize(
        data.get("response", []),
        record_path=["seasons"],
        meta=[
            ["league", "id"],
            ["league", "name"],
            ["league", "type"],
            ["league", "logo"],
            ["country", "name"],
            ["country", "code"],
            ["country", "flag"],
        ],
        sep="__"
    )

    # Clean/rename columns
    rename_map = {
        "league__id": "league_id",
        "league__name": "league_name",
        "league__type": "league_type",
        "league__logo": "league_logo",
        "country__name": "country_name",
        "country__code": "country_code",
        "country__flag": "country_flag",
        "year": "season_year",
        "start": "season_start",
        "end": "season_end",
        "current": "season_current",
        # fixtures coverage
        "coverage__fixtures__events": "cov_fixtures_events",
        "coverage__fixtures__lineups": "cov_fixtures_lineups",
        "coverage__fixtures__statistics_fixtures": "cov_fixtures_stats_fixtures",
        "coverage__fixtures__statistics_players": "cov_fixtures_stats_players",
        # other coverage flags
        "coverage__standings": "cov_standings",
        "coverage__players": "cov_players",
        "coverage__top_scorers": "cov_top_scorers",
        "coverage__top_assists": "cov_top_assists",
        "coverage__top_cards": "cov_top_cards",
        "coverage__injuries": "cov_injuries",
        "coverage__predictions": "cov_predictions",
        "coverage__odds": "cov_odds",
    }
    seasons_flat = seasons_flat.rename(columns=rename_map)

    # league_seasons_df: core season info + coverage
    keep_cols = [
        "league_id", "league_name", "league_type", "league_logo",
        "country_name", "country_code", "country_flag",
        "season_year", "season_start", "season_end", "season_current",
        "cov_fixtures_events", "cov_fixtures_lineups",
        "cov_fixtures_stats_fixtures", "cov_fixtures_stats_players",
        "cov_standings", "cov_players", "cov_top_scorers", "cov_top_assists",
        "cov_top_cards", "cov_injuries", "cov_predictions", "cov_odds",
    ]
    # Some keys may be missing in older seasons; fill them if absent
    for c in keep_cols:
        if c not in seasons_flat.columns:
            seasons_flat[c] = None
    league_seasons_df = seasons_flat[keep_cols].copy()

    # leagues_df: one row per league
    leagues_df = (
        league_seasons_df[
            ["league_id", "league_name", "league_type", "league_logo",
             "country_name", "country_code", "country_flag"]
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )


    # Types / sorting niceties
    league_seasons_df["season_year"] = pd.to_numeric(league_seasons_df["season_year"], errors="coerce")
    league_seasons_df = league_seasons_df.sort_values(["league_id", "season_year"]).reset_index(drop=True)

    return leagues_df, league_seasons_df





if __name__ == "__main__":
    json_path = "football-and-spark/data/json_data/all_leagues.json"
    leagues_df, league_seasons_df = get_all_leagues_parser(json_path)
    print(leagues_df.head())
    print(league_seasons_df.head())
    # Insert into SQLite
    db_path = os.path.join(os.path.dirname(__file__), '../database/football_data.db')
    insert_dataframe_to_table(db_path, leagues_df, 'leagues_stage')

# leagues_df.to_csv("football-and-spark/data/csv_data/leagues.csv", index=False)
# league_seasons_df.to_csv("football-and-spark/data/csv_data/league_seasons.csv", index=False)
