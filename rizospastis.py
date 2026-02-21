import requests
import os

# 1. Λήψη PDF
url = "https://sep.gr/wp-content/uploads/rizospastis_auto_replace/rizospastis_current.pdf"
headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://sep.gr/"}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    with open("rizospastis_current.pdf", "wb") as f:
        f.write(response.content)
    print("PDF Downloaded.")

    # 2. Ανέβασμα στο Dropbox
    token = os.environ.get("DROPBOX_TOKEN")
    if token:
        dbx_url = "https://content.dropboxapi.com/2/files/upload"
        dbx_headers = {
            "Authorization": f"Bearer {token}",
            "Dropbox-API-Arg": '{"path": "/rizospastis_current.pdf", "mode": "overwrite"}',
            "Content-Type": "application/octet-stream"
        }
        with open("rizospastis_current.pdf", "rb") as f:
            db_res = requests.post(dbx_url, headers=dbx_headers, data=f)
        
        if db_res.status_code == 200:
            print("Successfully uploaded to Dropbox!")
        else:
            print(f"Dropbox Error: {db_res.text}")
