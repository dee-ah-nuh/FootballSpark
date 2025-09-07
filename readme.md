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



erDiagram
    COUNTRY ||--o{ CITY : "has"
    CITY ||--o{ STADIUM : "hosts"
    CITY ||--o{ AIRPORT : "served by"

    LEAGUE ||--o{ SEASON : "contains"
    LEAGUE ||--o{ TEAM : "participates"
    TEAM ||--o{ PLAYER : "roster"
    TEAM ||--o{ TEAM_SEASON : "per-season meta"
    TEAM ||--o{ HOME_STADIUM : "plays at" 

    SEASON ||--o{ FIXTURE : "schedules"
    STADIUM ||--o{ FIXTURE : "at"
    TEAM ||--o{ FIXTURE_TEAM : "home/away"
    FIXTURE ||--o{ FIXTURE_TEAM : "has"
    FIXTURE ||--o{ LINEUP : "announced"
    PLAYER ||--o{ LINEUP_PLAYER : "selected"
    LINEUP ||--o{ LINEUP_PLAYER : "includes"

    PLAYER ||--o{ INJURY_REPORT : "status"
    TEAM ||--o{ TRANSFER_EVENT : "in/out"

    FIXTURE ||--o{ ATTENDANCE : "historical"
    FIXTURE ||--o{ TICKET_PRICE : "official/secondary"
    FIXTURE ||--o{ SOCIAL_METRIC : "hype/signals"
    FIXTURE ||--o{ ODDS : "bookmaker"
    FIXTURE ||--o{ MATCH_STAT : "box score"
    FIXTURE ||--o{ PREDICTION : "rating, demand, outcome"
    TEAM ||--o{ POPULARITY_BASELINE : "global fan base"
    PLAYER ||--o{ POPULARITY_BASELINE : "star power"

    PROVIDER ||--o{ FLIGHT_OFFER : "from APIs"
    PROVIDER ||--o{ HOTEL_OFFER : "from APIs"
    AIRPORT ||--o{ FLIGHT_OFFER : "origin/destination"
    CITY ||--o{ HOTEL_OFFER : "location"

    USER ||--o{ SEARCH_SESSION : "filters, dates"
    USER ||--o{ BOOKING_INTENT : "saved plan"
    SEARCH_SESSION ||--o{ MATCH_TRAVEL_OPTION : "ranked list"
    FIXTURE ||--o{ MATCH_TRAVEL_OPTION : "candidate"
    FLIGHT_OFFER ||--o{ MATCH_TRAVEL_OPTION : "paired"
    HOTEL_OFFER ||--o{ MATCH_TRAVEL_OPTION : "paired"
# football-and-spark
