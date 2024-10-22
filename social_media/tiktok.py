import webbrowser
import os

client_key = os.getenv("TIKTOK_CLIENT_KEY")  # Dein Client Key
redirect_uri = "https://ihsan06.github.io/takeiteasy/server/"  # Deine korrekte Redirect URI

auth_url = f"https://www.tiktok.com/auth/authorize/?client_key={client_key}&scope=user.info.basic,video.upload&response_type=code&redirect_uri={redirect_uri}&state=random_state"

# Öffne den Browser, um die OAuth-Seite zu öffnen
webbrowser.open(auth_url)



""" import requests

# Schritt 1: Upload-URL anfordern
url = "https://open-api.tiktok.com/share/video/upload/"
headers = {
    "Authorization": "Bearer YOUR_ACCESS_TOKEN"
}
data = {
    "open_id": "USER_OPEN_ID",  # Open ID des authentifizierten Benutzers
}

response = requests.post(url, headers=headers, data=data)
upload_url = response.json().get("data").get("upload_url")

# Schritt 2: Video an die Upload-URL senden
video_file_path = "path_to_your_video.mp4"

with open(video_file_path, "rb") as video_file:
    video_upload_response = requests.post(upload_url, files={"video": video_file})

print(video_upload_response.json())

"""