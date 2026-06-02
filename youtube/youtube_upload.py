
import os

from google.oauth2.credentials import Credentials

from googleapiclient.discovery import build

from googleapiclient.http import MediaFileUpload


TOKEN_FILE = "../auth/token.json"


def get_youtube_service():

    credentials = Credentials.from_authorized_user_file(
        TOKEN_FILE,
        [
            "https://www.googleapis.com/auth/youtube.upload"
        ]
    )

    return build(
        "youtube",
        "v3",
        credentials=credentials
    )


def upload_youtube_video(
    video_path,
    title,
    description,
    tags=None
):

    if tags is None:
        tags = []

    youtube = get_youtube_service()
    
    if "#shorts" not in title.lower():
        title += " #Shorts"
    
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "26"
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(
        video_path,
        resumable=True,
        chunksize=-1
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None

    while response is None:

        status, response = request.next_chunk()

        if status:
            print(
                f"Upload Progress: {int(status.progress() * 100)}%"
            )

    return response["id"]
