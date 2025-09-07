-- get leagues/cups (done)
    --- league id, league_name, type, country, dates_played, 
-- get team ids, information (done)
    --- id, name, abbreviation, founded, venue_id, venue, address, city, capacity, surface
-- get players information (done)
    -- nationality, team, stats
-- team season information 
    --- season, team, lezgue, form, yellow/red cards, lineup, fixtures, wins, losses, draws, 




-- NEED (TPES OF DATA):

Fixtures + Lineups + Match Stats + Odds + Attendance + Ticket Prices

Travel layer (stadiums geo, airports, flights, hotels)

Sentiment/hype signals (social + search trends)

Injuries / transfers


-- to do:
Fixtures (per season)
fixture_id, date, round, home_team_id, away_team_id, venue_id, referee, status
Purpose: anchor table for joining everything (tickets, odds, stats, travel).

Lineups (per fixture)
fixture_id, player_id, position, formation, minutes_played, rating
Purpose: star power + player availability features.

Match Statistics
fixture_id, team_id, shots_on, shots_off, possession, passes, fouls, cards, xG
Purpose: quality/intensity indicators.

Odds / Betting Markets
fixture_id, bookmaker, home_win, draw, away_win
Purpose: proxy for match expected competitiveness/popularity.

Historical Attendance
fixture_id, reported_attendance, stadium_capacity

