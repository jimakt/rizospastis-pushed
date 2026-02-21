import requests

url = "https://sep.gr/wp-content/uploads/rizospastis_auto_replace/rizospastis_current.pdf"
headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://sep.gr/"
}

filename = "rizospastis_current.pdf" # Σταθερό όνομα για να γίνεται overwrite

print("Downloading current edition...")
response = requests.get(url, headers=headers)

if response.status_code == 200:
    with open(filename, "wb") as f:
        f.write(response.content)
    print("Success: File updated.")
else:
    print(f"Failed: {response.status_code}")
