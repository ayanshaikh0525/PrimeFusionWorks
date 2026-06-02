from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/drive"]

# def get_drive_service():

#     credentials = service_account.Credentials.from_service_account_file(
#         "../auth/drive_service_account.json",
#         scopes=SCOPES
#     )

#     return build(
#         "drive",
#         "v3",
#         credentials=credentials
#     )


from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import os


def get_drive_service():
    creds = Credentials(
        None,
        refresh_token=os.environ["GOOGLE_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["GOOGLE_CLIENT_ID"],
        client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
        scopes=["https://www.googleapis.com/auth/drive"]
    )

    creds.refresh(Request())

    return build(
        "drive",
        "v3",
        credentials=creds
    )

# List Files In Folder

def list_files(folder_id):

    service = get_drive_service()

    results = service.files().list(
        q=f"'{folder_id}' in parents and trashed=false",
        fields="files(id,name)"
    ).execute()

    return results.get("files", [])


# Download Video

import io

from googleapiclient.http import MediaIoBaseDownload


def download_file(
    file_id,
    destination_path
):
    service = get_drive_service()

    request = service.files().get_media(
        fileId=file_id
    )

    fh = io.FileIO(
        destination_path,
        "wb"
    )

    downloader = MediaIoBaseDownload(
        fh,
        request
    )

    done = False

    while not done:
        _, done = downloader.next_chunk()

    return destination_path

# Upload File

from googleapiclient.http import MediaFileUpload


def upload_file(
    local_path,
    folder_id
):

    service = get_drive_service()

    metadata = {
        "name": local_path.split("/")[-1],
        "parents": [folder_id]
    }

    media = MediaFileUpload(
        local_path,
        resumable=True
    )

    file = service.files().create(
        body=metadata,
        media_body=media,
        fields="id"
    ).execute()

    return file["id"]



# Delete File

def delete_file(file_id):

    service = get_drive_service()

    service.files().delete(
        fileId=file_id
    ).execute()


# Generate Drive Link

def get_drive_link(file_id):

    return (
        f"https://drive.google.com/file/d/"
        f"{file_id}/view"
    )



# Download Processed Video

def download_processed_video(
    video_record,
    output_path
):

    download_file(
        video_record["processed"]["drive_file_id"],
        output_path
    )

    return output_path
