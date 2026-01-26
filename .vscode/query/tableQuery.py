import sqlite3
import pandas as pd

DB_FILE = "data/football.db"

conn = sqlite3.connect(DB_FILE)

query = """
WITH all_teams AS (
    SELECT home_team AS team, 
           home_goals AS goals_for, away_goals AS goals_against,
           CASE 
               WHEN home_goals > away_goals THEN 1 ELSE 0 END AS win,
           CASE 
               WHEN home_goals = away_goals THEN 1 ELSE 0 END AS draw,
           CASE 
               WHEN home_goals < away_goals THEN 1 ELSE 0 END AS loss
    FROM matches
    UNION ALL
    SELECT away_team AS team, 
           away_goals AS goals_for, home_goals AS goals_against,
           CASE 
               WHEN away_goals > home_goals THEN 1 ELSE 0 END AS win,
           CASE 
               WHEN away_goals = home_goals THEN 1 ELSE 0 END AS draw,
           CASE 
               WHEN away_goals < home_goals THEN 1 ELSE 0 END AS loss
    FROM matches
)
SELECT 
    team,
    COUNT(*) AS played,
    SUM(win) AS wins,
    SUM(draw) AS draws,
    SUM(loss) AS losses,
    SUM(goals_for) AS goals_for,
    SUM(goals_against) AS goals_against,
    SUM(goals_for) - SUM(goals_against) AS goal_diff,
    SUM(win)*3 + SUM(draw) AS points
FROM all_teams
GROUP BY team
ORDER BY points DESC, goal_diff DESC, goals_for DESC
"""

df = pd.read_sql_query(query, conn)
conn.close()

# Save the league table
df.to_csv("data/processed/league_table_sql.csv", index=False)
print("League table generated via SQL and saved!")
print(df.head(10))
