CREATE TABLE IF NOT EXISTS leagues_stage (
    league_id VARCHAR(32) NOT NULL,
    league_name VARCHAR(255) NOT NULL,
    league_type VARCHAR(64) NOT NULL,
    league_logo VARCHAR(512) NOT NULL,
    country_name VARCHAR(128) NOT NULL,
    country_code VARCHAR(16),
    country_flag VARCHAR(512)
);