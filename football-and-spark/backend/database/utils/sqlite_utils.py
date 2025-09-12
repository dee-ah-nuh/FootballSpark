# sqlite_utils.py
import os
import sqlite3
import logging
from pathlib import Path
import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

DB_PATH = os.getenv("FOOTBALL_DB_PATH")

if not DB_PATH:
    this_file = Path(__file__).resolve()
    parts = list(this_file.parts)
    if "football-and-spark" in parts:
        root_idx = parts.index("football-and-spark")
        REPO_ROOT = Path(*parts[: root_idx + 1])
    else:
        REPO_ROOT = this_file.parents[1]

    DB_PATH = str(REPO_ROOT / "backend" / "database" / "football_data.db")

DB_PATH = Path(DB_PATH)

logger.info(f"sqlite_utils initialized with DB_PATH={DB_PATH}")


def insert_dataframe_to_stage_table(db_path, df, table_name):
    """
    Inserts a pandas DataFrame into the specified SQLite table.
    """
    db_path = Path(db_path).resolve()
    logger.info(f"insert_dataframe_to_stage_table called")
    logger.info(f"Resolved db_path={db_path}")
    logger.info(f"Files under {db_path.parent}: {list(db_path.parent.glob('*'))}")

    try:
        conn = sqlite3.connect(str(db_path))
        logger.info(f"Connected to database at {db_path}")
    except Exception as e:
        logger.error(f"Failed to connect to SQLite at {db_path}: {e}", exc_info=True)
        raise

    try:
        conn.execute(f"DELETE FROM {table_name};")
        logger.info(f"Deleted all rows from table {table_name}")
    except sqlite3.OperationalError as e:
        logger.warning(f"Could not truncate table {table_name}: {e}")

    try:
        df.to_sql(table_name, conn, if_exists="append", index=False)
        logger.info(f"Inserted {len(df)} rows into {table_name}")
    except Exception as e:
        logger.error(f"Error inserting into {table_name}: {e}", exc_info=True)
        raise
    finally:
        conn.close()
        logger.info("Connection closed")
