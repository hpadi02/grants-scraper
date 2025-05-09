import requests
import xml.etree.ElementTree as ET
import csv
from datetime import datetime

# URL for Grants.gov RSS feed with new opportunities
rss_url = "https://www.grants.gov/rss/GGNewOpportunities.xml"

# Download the RSS feed
print("Downloading RSS feed...")
response = requests.get(rss_url)
if response.status_code != 200:
    raise Exception(f"Failed to download RSS feed: {response.status_code} {response.text}")

# Parse the XML content
print("Parsing RSS feed...")
root = ET.fromstring(response.content)

items = root.findall(".//item")
print(f"Found {len(items)} grant opportunities.")

# Save parsed items to a CSV file
today = datetime.utcnow().date()
filename = f"rss_grants_{today}.csv"
with open(filename, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Link", "Description", "Post Date"])
    for item in items:
        title = item.findtext("title", default="")
        link = item.findtext("link", default="")
        description = item.findtext("description", default="")
        pub_date = item.findtext("pubDate", default="")
        writer.writerow([title, link, description, pub_date])

print(f"Saved {len(items)} opportunities to {filename}")