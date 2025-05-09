import requests
import zipfile
import io
import os
from datetime import datetime

# URL of the ZIP file containing grant opportunities
zip_url = "https://www.grants.gov/download/opportunities/GrantsDBExtract.zip"

# Download the ZIP file
print("Downloading grants ZIP archive...")
response = requests.get(zip_url)
if response.status_code != 200:
    raise Exception(f"Failed to download ZIP file: {response.status_code} {response.text}")

# Extract the ZIP file
print("Extracting ZIP archive...")
with zipfile.ZipFile(io.BytesIO(response.content)) as z:
    extract_dir = f"grants_extract_{datetime.utcnow().date()}"
    os.makedirs(extract_dir, exist_ok=True)
    z.extractall(path=extract_dir)

print(f"ZIP file extracted to '{extract_dir}'. Contents:")
for filename in os.listdir(extract_dir):
    print("-", filename)