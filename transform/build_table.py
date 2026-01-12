import csv
from collections import defaultdict

INPUT_FILE = "data/processed/matches_clean.csv"
OUTPUT_FILE = "data/processed/league_table.csv"

def new_team():
    return{
        "played": 0,
        "wins": 0,
        "draws": 0,
        "losses": 0,
        "goals_for": 0,
        "goals_against": 0,
        "goal_diff": 0,
        "points": 0
    }

table = defaultdict(new_team)

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        home = row["home_team"]
        away = row["away_team"]

        home_goals = int(row["home_goals"])
        away_goals = int(row["away_goals"])

        table[home]["played"] += 1
        table[away]["played"] += 1

        table[home]["goals_for"] += home_goals
        table[home]["goals_against"] += away_goals

        if home_goals > away_goals:
            table[home]["wins"] += 1
            table[away]["losses"] += 1
            table[home]["points"] += 3
        elif home_goals < away_goals:
            table[away]["wins"] += 1
            table[home]["losses"] += 1
            table[away]["points"] += 3
        else:
            table[home]["draws"] += 1
            table[away]["draws"] += 1
            table[home]["points"] += 1
            table[away]["points"] += 1

for team in table:
    table[team]["goal_diff"] = (
    table[team]["goals_for"] - table[team]["goals_against"]
    )

sorted_table = sorted(
    table.items(),
    key=lambda x: (
        x[1]["points"],
        x[1]["goal_diff"],
        x[1]["goals_for"],
    ),
    reverse=True
)

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    fieldnames=["team"] + list(sorted_table[0][1].keys())
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for team, stats in sorted_table:
        writer.writerow({"team": team, **stats})

print(f"League table saved to {OUTPUT_FILE}")

