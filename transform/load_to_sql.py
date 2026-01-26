import sqlite3
import csv

DB_FILE = "data/football.db"
MATCHES_CSV = "data/processed/matches_clean.csv"


conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()


cursor.execute("DROP TABLE IF EXISTS matches")


cursor.execute("""
CREATE TABLE matches (
    match_id INTEGER PRIMARY KEY,
    utc_date TEXT,
    season INTEGER,
    competition TEXT,
    home_team TEXT,
    away_team TEXT,
    home_goals INTEGER,
    away_goals INTEGER,
    match_status TEXT
)
""")


with open(MATCHES_CSV, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = [
        (
            int(row["match_id"]),
            row["utc_date"],
            int(row["season"]),
            row["competition"],
            row["home_team"],
            row["away_team"],
            int(row["home_goals"]) if row["home_goals"] != "" else None,
            int(row["away_goals"]) if row["away_goals"] != "" else None,
            row["match_status"]
        )
        for row in reader
    ]

cursor.executemany("""
INSERT INTO matches (
    match_id, utc_date, season, competition, home_team, away_team,
    home_goals, away_goals, match_status
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", rows)

conn.commit()
conn.close()

print(f"Loaded {len(rows)} matches into {DB_FILE}")
