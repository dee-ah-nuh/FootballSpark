import http.client
import json 
import os 
import pandas as pd
import sqlite3
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../database/utils'))
from sqlite_utils import insert_dataframe_to_stage_table  # type: ignore

# Fetch all leagues from API-Football and save to JSON
def get_all_leagues():
    """
    Fetches all leagues from the API-Football and saves to a JSON file.
    """
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "1c4235d512452af307933a9088a514d9"
    }

    conn.request("GET", "/leagues", headers=headers)

    res = conn.getresponse()
    data = res.read()
    # data = data.decode("utf-8")

    print(data)

    data = json.loads(data)

    return data
# Parse the leagues JSON into two DataFrames: leagues_df and league_seasons_df
def get_all_leagues_parser(data):
    """
    Loads the API-Football leagues JSON and returns:
      - leagues_df: one row per league
      - league_seasons_df: one row per (league_id, season_year) with flattened coverage flags
    """
    if not data:
        raise ValueError("No data provided")

    # data = json.loads(data)

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
# Simple SQLite helpers to get/insert leagues data for FastAPI
def sqlite_get_all_leagues():
    db_path = os.path.join(os.path.dirname(__file__), '../../backend/database/football_data.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT league_id, league_name, country_name, country_code, league_type, league_logo FROM leagues_stage")
    rows = cursor.fetchall()
    conn.close()

    # Convert rows to list of dicts
    leagues = [
        {
            "league_id": row[0],
            "league_name": row[1],
            "country_name": row[2],
            "country_code": row[3],
            "league_type": row[4],
            "league_logo": row[5]
        }
        for row in rows
    ]
    return leagues
# Insert leagues into SQLite
def sqlite_insert_leagues(leagues):
    db_path = os.path.join(os.path.dirname(__file__), '../database/football_data.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    for league in leagues:
        cursor.execute("""
            INSERT OR REPLACE INTO leagues_stage (league_id, league_name, country_name, country_code, league_type, league_logo)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            league.league_id,
            league.league_name,
            league.country_name,
            league.country_code,
            league.league_type,
            league.league_logo
        ))
    conn.commit()
    conn.close()
# Full ETL function to fetch, parse, and insert leagues data
def get_leagues_etl(db_path=None):

    # 1. Fetch data
    data = get_all_leagues()

    # 2. Parse data
    leagues_df, league_seasons_df = get_all_leagues_parser(data)
    print(leagues_df.head())
    print(league_seasons_df.head())


    # 3. Insert into SQLite
    sys.path.append(os.path.join(os.path.dirname(__file__), '../database/utils'))
    from sqlite_utils import insert_dataframe_to_stage_table  # type: ignore

    if db_path:
        insert_dataframe_to_stage_table(db_path, leagues_df, 'leagues_stage')
        
    elif db_path is None:
        db_path = os.path.join(os.path.dirname(__file__), '../../database/football_data.db')
        insert_dataframe_to_stage_table(db_path, leagues_df, 'leagues_stage')

# db_path = os.path.join(os.path.dirname(__file__), '../database/football_data.db')
# get_leagues_etl(db_path=db_path)
