# gdrive_utils.py
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import io
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

# Google Drive API scopes
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate_gdrive():
    """Authenticates and returns the Google Drive service."""
    creds = None
    # The file token.json stores the user's access and refresh tokens
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If credentials are not valid or don't exist, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    # Return the Google Drive API service
    return build('drive', 'v3', credentials=creds)

def list_audio_files(service, folder_id):
    query = f"'{folder_id}' in parents and trashed = false and mimeType contains 'audio/'"
    response = service.files().list(q=query, fields="files(id, name)").execute()
    return response.get('files', [])

def download_file(service, file_id, file_name, local_path):
    """Downloads a file from Google Drive to a local path."""
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    with open(local_path, 'wb') as f:
        f.write(fh.getvalue())
    return local_path

def move_file(service, file_id, new_folder_id):
    """Moves a file to a new folder in Google Drive."""
    file = service.files().get(fileId=file_id, fields='parents').execute()
    previous_parents = ",".join(file.get('parents'))
    file = service.files().update(
        fileId=file_id,
        addParents=new_folder_id,
        removeParents=previous_parents,
        fields='id, parents'
    ).execute()
    return file