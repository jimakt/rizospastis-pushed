import requests
import os
import sys

# Λήψη στοιχείων από τα Secrets
APP_KEY = os.environ.get("DBX_APP_KEY")
APP_SECRET = os.environ.get("DBX_APP_SECRET")
REFRESH_TOKEN = os.environ.get("DBX_REFRESH_TOKEN")

print("--- Starting Execution ---")

# 1. Λήψη PDF
url = "https://sep.gr/wp-content/uploads/rizospastis_auto_replace/rizospastis_current.pdf"
try:
    print(f"Downloading from: {url}")
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    response.raise_for_status()
    with open("rizospastis_current.pdf", "wb") as f:
        f.write(response.content)
    print("PDF downloaded successfully.")
except Exception as e:
    print(f"Download Error: {e}")
    sys.exit(1)

# 2. Λήψη Access Token
print("Requesting Access Token from Dropbox...")
token_url = "https://api.dropbox.com/oauth2/token"
token_data = {
    "grant_type": "refresh_token",
    "refresh_token": REFRESH_TOKEN
}
try:
    token_res = requests.post(token_url, data=token_data, auth=(APP_KEY, APP_SECRET), timeout=20)
    token_res.raise_for_status()
    access_token = token_res.json().get("access_token")
    print("Access Token acquired.")
except Exception as e:
    print(f"Token Error: {e}")
    if 'token_res' in locals(): print(f"Response: {token_res.text}")
    sys.exit(1)

# 3. Ανέβασμα στο Dropbox
print("Uploading to Dropbox...")
dbx_url = "https://content.dropboxapi.com/2/files/upload"
dbx_headers = {
    "Authorization": f"Bearer {access_token}",
    "Dropbox-API-Arg": '{"path": "/rizospastis_current.pdf", "mode": "overwrite", "mute": true}',
    "Content-Type": "application/octet-stream"
}

try:
    with open("rizospastis_current.pdf", "rb") as f:
        upload_res = requests.post(dbx_url, headers=dbx_headers, data=f, timeout=60)
    
    if upload_res.status_code == 200:
        result = upload_res.json()
        print("--- SUCCESS ---")
        print(f"File Path in Dropbox: {result.get('path_display')}")
    else:
        print(f"Upload failed with status {upload_res.status_code}")
        print(f"Dropbox Message: {upload_res.text}")
except Exception as e:
    print(f"Upload Error: {e}")
    sys.exit(1)
