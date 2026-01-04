import json
import csv
from datetime import datetime

RAW_FILE = "data/matches_2026-01-04.json"
OUTPUT_FILE = "data/processed/matches_clean.csv"

with open(RAW_FILE, 'r', encoding="utf-8") as f:
    raw_data = json.load(f)

matches = raw_data["matches"]

print("total matches:", len(matches))

clean_rows = []

for match in matches:
    if match.get("status") != "FINISHED":
        continue
    score = match.get("score", {}).get("fullTime",{})
    row = {
        "match_id": match["id"],
        "utc_date": match["utcDate"],
        "season": match["season"]["startDate"][:4],
        "competition": match["competition"]["name"],
        "home_team": match["homeTeam"]["name"],
        "away_team": match["awayTeam"]["name"],
        "home_goals": match["score"]["fullTime"]["home"],
        "away_goals": match["score"]["fullTime"]["away"],
        "match_status": match["status"]
    }
    clean_rows.append(row)

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f,fieldnames=clean_rows[0].keys())
    writer.writeheader()
    writer.writerows(clean_rows)

print(f"saved cleaned data to {OUTPUT_FILE}")
