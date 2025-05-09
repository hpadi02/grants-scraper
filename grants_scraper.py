import requests
import feedparser
import csv
from datetime import datetime

# URL for Grants.gov RSS feed with new opportunities
rss_url = "https://www.grants.gov/rss/GGNewOpportunities.xml"

# Download and parse the RSS feed using feedparser
print("Downloading and parsing RSS feed...")
feed = feedparser.parse(rss_url)

if feed.bozo:
    print(f"Warning: RSS parsing error: {feed.bozo_exception}")
    if not feed.entries:
        raise Exception("No valid entries could be parsed from the RSS feed.")

print(f"Found {len(feed.entries)} grant opportunities.")

# Save parsed items to a CSV file
today = datetime.utcnow().date()
filename = f"rss_grants_{today}.csv"
with open(filename, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Link", "Description", "Post Date"])
    for entry in feed.entries:
        writer.writerow([
            entry.get("title", ""),
            entry.get("link", ""),
            entry.get("description", ""),
            entry.get("published", "")
        ])

print(f"Saved {len(feed.entries)} opportunities to {filename}")