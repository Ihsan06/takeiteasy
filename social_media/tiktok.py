import webbrowser
import os

# Die OAuth2 URL, um den Benutzer zur TikTok-Berechtigung weiterzuleiten
client_key = os.getenv("TIKTOK_CLIENT_KEY")
redirect_uri = "http://localhost:8000/callback"  # Dein Redirect-URI

auth_url = f"https://www.tiktok.com/auth/authorize/?client_key=awzlrwqeofy44hnl&scope=user.info.basic,video.upload&response_type=code&redirect_uri={redirect_uri}&state=some_random_state"

# Öffne den Browser, um die Erlaubnis anzufordern
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