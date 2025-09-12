# dags/test_sqlite_connection_dag.py
from __future__ import annotations

import sqlite3
from datetime import datetime

from airflow.decorators import dag, task
from airflow.hooks.base import BaseHook

CONN_ID = "sqlite_football"  # Airflow Connection (SQLite). Set Schema to absolute .db path.


@dag(
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["sqlite", "connection", "test"],
)
def test_sqlite_connection():
    @task
    def make_data() -> list[tuple]:
        """
        Rows match DDL:
        (league_id, league_name, league_type, league_logo, country_name, country_code, country_flag)
        """
        return [
            (
                "39",
                "Premier League",
                "League",
                "https://media.api-sports.io/football/leagues/39.png",
                "England",
                "GB",
                "https://media.api-sports.io/flags/gb.svg",
            ),
            (
                "140",
                "La Liga",
                "League",
                "https://media.api-sports.io/football/leagues/140.png",
                "Spain",
                "ES",
                "https://media.api-sports.io/flags/es.svg",
            ),
            (
                "135",
                "Serie A",
                "League",
                "https://media.api-sports.io/football/leagues/135.png",
                "Italy",
                "IT",
                "https://media.api-sports.io/flags/it.svg",
            ),
        ]

    @task
    def insert_rows(rows: list[tuple]) -> str:
        # Resolve DB file path from Airflow Connection
        conn = BaseHook.get_connection(CONN_ID)
        db_path = conn.schema or conn.host or conn.extra_dejson.get("path")
        if not db_path:
            raise RuntimeError(
                f"Could not resolve SQLite file path from connection `{CONN_ID}`. "
                "Set Schema to the absolute .db file path (e.g. /opt/airflow/.../football_data.db)."
            )

        with sqlite3.connect(db_path, timeout=30) as cx:
            cx.execute(
                """
                CREATE TABLE IF NOT EXISTS leagues_stage2 (
                    league_id VARCHAR(32) NOT NULL,
                    league_name VARCHAR(255) NOT NULL,
                    league_type VARCHAR(64) NOT NULL,
                    league_logo VARCHAR(512) NOT NULL,
                    country_name VARCHAR(128) NOT NULL,
                    country_code VARCHAR(16),
                    country_flag VARCHAR(512)
                )
                """
            )
            # Clear for test repeatability
            # cx.execute("DELETE FROM leagues_stage")
            cx.executemany(
                """
                INSERT INTO leagues_stage2 (
                    league_id, league_name, league_type, league_logo,
                    country_name, country_code, country_flag
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                rows,
            )
            cx.commit()
        return db_path

    @task
    def verify_rows(db_path: str) -> int:
        with sqlite3.connect(db_path, timeout=30) as cx:
            cur = cx.execute("SELECT COUNT(*) FROM leagues_stage2")
            (count,) = cur.fetchone()
            print(f"[verify] leagues_stage row count = {count} (db: {db_path})")
            return count

    verify_rows(insert_rows(make_data()))


test_sqlite_connection()
