from __future__ import print_function

import os.path
from typing import List, Optional

from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = [
    "https://www.googleapis.com/auth/drive.metadata.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]

ALLOWED_MIME_TYPES: dict[str] = {
    "application": "application/",
    "image": "image/",
    "video": "video/",
    "audio": "audio/",
    "text": "text/",
}


class GoogleDriveAPI:
    def __init__(
        self,
        credentials_file: str = "apps/google_drive/credentials.json",
        token_file: str = "token.json",
    ):
        self.credentials_file = credentials_file
        self.token_file = token_file

    def get_credentials(self) -> Credentials:
        creds = None
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open(self.token_file, "w") as token:
                token.write(creds.to_json())
        return creds

    def search_files(
        self, name_query: str, mime_type: Optional[str] = None
    ) -> List[dict]:
        """List all"""
        creds = self.get_credentials()
        service = build("drive", "v3", credentials=creds)

        try:
            query = ""
            if name_query:
                query += f"name contains '{name_query}'"
            allowed_mime_type = self.get_mime_type(mime_type)

            if allowed_mime_type:
                and_query = "and " if name_query else ""
                query += f"{and_query}mimeType contains '{allowed_mime_type}'"
            print(query)
            results = (
                service.files()
                .list(
                    pageSize=20,
                    q=query,
                    fields="nextPageToken, files(id, name, thumbnailLink, webContentLink, mimeType, fileExtension)",
                )
                .execute()
            )
            items = results.get("files", [])
            return items
        except HttpError as error:
            print(f"An error occurred: {error}")
            return []

    def create_drive_service(self):
        credentials = self.get_credentials()
        drive_service = build("drive", "v3", credentials=credentials)
        return drive_service

    def get_mime_type(self, mime_type: str) -> str:
        return ALLOWED_MIME_TYPES.get(mime_type)


gdrive_api = GoogleDriveAPI()
