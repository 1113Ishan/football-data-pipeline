import sqlite3

DB_FILE = "data/football.db"

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()


cursor.execute("SELECT COUNT(*) FROM matches")
print("Total matches:", cursor.fetchone()[0])


cursor.execute("""
SELECT home_team, COUNT(*) as home_matches
FROM matches
GROUP BY home_team
ORDER BY home_matches DESC
""")
print("\nMatches per team (home):")
for row in cursor.fetchall():
    print(row)


cursor.execute("""
SELECT home_team, SUM(home_goals) as goals
FROM matches
GROUP BY home_team
ORDER BY goals DESC
""")
print("\nTop scoring home teams:")
for row in cursor.fetchall():
    print(row)

conn.close()
