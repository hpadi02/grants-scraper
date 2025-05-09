import requests
import zipfile
import io
import os
from datetime import datetime

# URL of the ZIP file containing grant opportunities
zip_url = "https://www.grants.gov/download/opportunities/GrantsDBExtract.zip"

# Download the ZIP file
print("Downloading grants ZIP archive...")
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}
response = requests.get(zip_url, headers=headers)
if response.status_code != 200:
    raise Exception(f"Failed to download ZIP file: {response.status_code} {response.text}")

content_type = response.headers.get("Content-Type", "")
if "zip" not in content_type:
    raise Exception(f"Expected a ZIP file, but got Content-Type: {content_type}")

# Extract the ZIP file
print("Extracting ZIP archive...")
try:
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        extract_dir = f"grants_extract_{datetime.utcnow().date()}"
        os.makedirs(extract_dir, exist_ok=True)
        z.extractall(path=extract_dir)
except zipfile.BadZipFile:
    raise Exception("Downloaded file is not a valid ZIP archive.")

print(f"ZIP file extracted to '{extract_dir}'. Contents:")
for filename in os.listdir(extract_dir):
    print("-", filename)