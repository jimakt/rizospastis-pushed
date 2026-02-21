import requests
import os

# Στοιχεία από το GitHub Secrets
APP_KEY = os.environ.get("DBX_APP_KEY")
APP_SECRET = os.environ.get("DBX_APP_SECRET")
REFRESH_TOKEN = os.environ.get("DBX_REFRESH_TOKEN")

# 1. Λήψη PDF
url = "https://sep.gr/wp-content/uploads/rizospastis_auto_replace/rizospastis_current.pdf"
response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

if response.status_code == 200:
    with open("rizospastis_current.pdf", "wb") as f:
        f.write(response.content)
    print("PDF downloaded.")

    # 2. Λήψη προσωρινού Access Token χρησιμοποιώντας το Refresh Token
    token_url = "https://api.dropbox.com/oauth2/token"
    token_data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN
    }
    token_res = requests.post(token_url, data=token_data, auth=(APP_KEY, APP_SECRET))
    access_token = token_res.json().get("access_token")

    if access_token:
        # 3. Ανέβασμα στο Dropbox (Overwrite)
        dbx_url = "https://content.dropboxapi.com/2/files/upload"
        dbx_headers = {
            "Authorization": f"Bearer {access_token}",
            "Dropbox-API-Arg": '{"path": "/rizospastis_current.pdf", "mode": "overwrite", "mute": true}',
            "Content-Type": "application/octet-stream"
        }
        with open("rizospastis_current.pdf", "rb") as f:
            upload_res = requests.post(dbx_url, headers=dbx_headers, data=f)
        
        if upload_res.status_code == 200:
            print("Success! PDF updated in Dropbox.")
        else:
            print(f"Upload failed: {upload_res.text}")
    else:
        print("Could not get access token.")
