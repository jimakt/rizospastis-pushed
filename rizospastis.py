import requests
from datetime import datetime
import os

url = "https://sep.gr/wp-content/uploads/rizospastis_auto_replace/rizospastis_current.pdf"
headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://sep.gr/"
}

# Δημιουργία ονόματος με ημερομηνία
date_str = datetime.now().strftime("%Y-%m-%d")
filename = f"rizospastis_{date_str}.pdf"

print(f"Downloading {filename}...")

response = requests.get(url, headers=headers)
if response.status_code == 200:
    with open(filename, "wb") as f:
        f.write(response.content)
    print("Done!")
else:
    print(f"Failed: {response.status_code}")
