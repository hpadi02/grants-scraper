import requests
import csv
from datetime import datetime, timedelta

# Grants.gov Search endpoint (POST)
endpoint = "https://www.grants.gov/grantsws/rest/opportunities/search"

# Get yesterday's date
today = datetime.utcnow().date()
yesterday = today - timedelta(days=1)

# Search payload — use POST instead of GET
payload = {
    "startRecordNum": 0,
    "oppStatuses": ["forecasted", "posted"],
    "modifiedFromDate": str(yesterday),
    "modifiedToDate": str(today),
    "rows": 100
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(endpoint, json=payload, headers=headers)

# Check the response
if response.status_code != 200:
    raise Exception(f"Failed to fetch data: {response.status_code} {response.text}")

data = response.json()
opportunities = data.get("oppHits", [])

filename = f"grants_{today}.csv"
with open(filename, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Opportunity ID", "Title", "Agency", "Open Date", "Close Date"])
    for opp in opportunities:
        writer.writerow([
            opp.get("cfdaNumber", ""),
            opp.get("title", ""),
            opp.get("agency", ""),
            opp.get("openDate", ""),
            opp.get("closeDate", "")
        ])

print(f"Saved {len(opportunities)} opportunities to {filename}")