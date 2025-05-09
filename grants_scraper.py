# grants_scraper.py
import requests
import csv
from datetime import datetime, timedelta

# Grants.gov API endpoint
endpoint = "https://www.grants.gov/grantsws/rest/opportunities/search"

# Get yesterday's date (or today)
today = datetime.utcnow().date()
yesterday = today - timedelta(days=1)

params = {
    "startRecordNum": 0,
    "oppStatuses": "forecasted,posted",  # You can change this
    "modifiedFromDate": str(yesterday),  # Get modified grants since yesterday
    "modifiedToDate": str(today),
    "rows": 100,
}

response = requests.get(endpoint, params=params)
data = response.json()

opportunities = data.get("oppHits", [])

# Save to CSV
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