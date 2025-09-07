| Function Name        | Purpose                                                    | Documentation Anchor (Endpoint) |
| -------------------- | ---------------------------------------------------------- | ------------------------------- |
| `countries_endpoint` | Lists all countries in the API coverage                    | `/tag/Countries`                |
| `seasons_endpoint`   | Lists seasons (year-based data for leagues)                | `/tag/Seasons`                  |
| `leagues_endpoint`   | League-level information (IDs, names, maybe logos, etc.)   | `/tag/Leagues`                  |
| `teams_endpoint`     | Teams in a league or by season                             | `/tag/Teams`                    |
| `standings_endpoint` | League standings                                           | `/tag/Standings`                |
| `fixtures_endpoint`  | Match schedules, upcoming or historical fixtures           | `/tag/Fixtures`                 |
| `events_endpoint`    | Detailed event data per fixture (goals, cards, lineups...) | `/tag/Events`                   |
| `odds_endpoint`      | Betting odds (live/pre-match, bookmakers)                  | `/tag/Odds`                     |




FootballSpark/
│
├── docker-compose.yaml
├── football-and_spark.html #Sample Front Page 
├── readme.md
├── requirements.txt
│
├── config/
│   └── airflow.cfg
│
├── football-and-spark/
│   ├── backend/
│   │   └── data/
│   │       ├── get_all_leagues.py
│   │       ├── ... (other data scripts)
│   │       ├── csv_data/
│   │       └── json_data/
│   ├── database/
│   │   ├── football_data.db
│   │   ├── db_setup.py
│   │   ├── football_sql/
│   │   │   ├── leagues.sql
│   │   │   ├── leagues_stage.sql
│   │   │   └── ... (other SQL files)
│   │   └── utils/
│   │       └── sqlite_utils.py
│   ├── frontend/
│   │   ├── main.py                # FastAPI backend
│   │   ├── static/
│   │   │   └── leagues.html       # Standalone HTML/JS frontend
│   │   └── web/                   # Next.js frontend app
│   │       ├── public/
│   │       └── src/
│   │           └── app/
│   │               ├── page.tsx
│   │               ├── layout.tsx
│   │               └── ... (other Next.js files)
│
└── dags/
    └── load_leagues_dag.py