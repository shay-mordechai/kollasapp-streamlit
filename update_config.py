import sys
import json
import base64
import requests

# Professional comment: Configuration
TOKEN = "YOUR_GITHUB_TOKEN"
REPO = "shay-mordechai/kollasapp-streamlit"
FILE_PATH = "server_config.json"
URL_TO_SAVE = sys.argv[1]

def update_github():
    headers = {"Authorization": f"token {TOKEN}"}
    api_url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"
    
    # 1. Get the current file SHA
    r = requests.get(api_url, headers=headers)
    if r.status_code != 200:
        print(f"Error: Could not find file. Status: {r.status_code}")
        return

    sha = r.json()['sha']
    
    # 2. Prepare the new content
    data = {"MUSIC_SERVER_URL": URL_TO_SAVE}
    content_base64 = base64.b64encode(json.dumps(data).encode()).decode()
    
    # 3. Update the file
    payload = {
        "message": f"Auto-update URL to {URL_TO_SAVE}",
        "content": content_base64,
        "sha": sha
    }
    
    update_r = requests.put(api_url, headers=headers, json=payload)
    if update_r.status_code == 200:
        print(f"Successfully updated GitHub with: {URL_TO_SAVE}")
    else:
        print(f"Failed to update. Status: {update_r.status_code}, Response: {update_r.text}")

if __name__ == "__main__":
    update_github()
