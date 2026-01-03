import requests
import json
from datetime import datetime

url = "https://api.football-data.org/v4/competitions/PL/matches"

Headers ={
    "X-Auth-Token": "603af97f9679473ebb26fde30761871e"
}
response = requests.get(url, headers=Headers)

today = datetime.today().strftime('%Y-%m-%d')
file_path = f"data/matches_{today}.json"


print("Status_code:", response.status_code)
print("response:", response.text[:500])
data = response.json()

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(data.keys())
print(f"Data saved to {file_path}") 


