# sqlite_utils.py (or central settings module)
from pathlib import Path
import os

# Prefer env override in case you move it later
DB_PATH = os.getenv("FOOTBALL_DB_PATH")
if not DB_PATH:
    # get_all_leagues.py is football-and-spark/backend/data/...
    # repo root is two levels up from that file location at runtime
    this_file = Path(__file__).resolve()
    # sqlite_utils.py is probably under .../football-and-spark/database/utils/,
    # so going up two levels lands at .../football-and-spark/database/
    # To be robust across callers, compute from project root instead:
    # Find the 'football-and-spark' dir in the path and build from there
    parts = list(this_file.parts)
    if "football-and-spark" in parts:
        root_idx = parts.index("football-and-spark")
        REPO_ROOT = Path(*parts[: root_idx + 1])
    else:
        # fallback to two parents – adjust if your layout differs
        REPO_ROOT = this_file.parents[2]

    DB_PATH = str(REPO_ROOT / "database" / "football_data.db")

DB_PATH = Path(DB_PATH)
DB_PATH.parent.mkdir(parents=True, exist_ok=True)  # ensure directory exists


import sqlite3
import os
import pandas as pd

def insert_dataframe_to_stage_table(db_path, df, table_name):
    """
    Inserts a pandas DataFrame into the specified SQLite table.
    """
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(f"DELETE FROM {table_name};")
        print(f"Deleted all rows from table {table_name}.")
    except sqlite3.OperationalError as e:
        print(f"Could not truncate table {table_name}: {e}")
    try:
        df.to_sql(table_name, conn, if_exists='append', index=False)
        print(f"Inserted {len(df)} rows into {table_name}.")
    except Exception as e:
        print(f"Error inserting into {table_name}: {e}")
    finally:
        conn.close()
