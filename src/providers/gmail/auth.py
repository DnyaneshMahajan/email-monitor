from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

from src.config.paths import ( 
    CREDENTIALS_FILE, 
    TOKEN_FILE,
)

from src.config.settings import (
    GMAIL_SCOPES,
)

def get_credentials() -> Credentials:
    """
    Authenticate with Gmail and return OAuth credentials

    Returns:
        Credentials: The user's Gmail API credentials.
    """
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(
            str(TOKEN_FILE), 
            GMAIL_SCOPES)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), 
                GMAIL_SCOPES,
                )
            
            creds = flow.run_local_server(port=0)

        TOKEN_FILE.write_text(creds.to_json())
            
    return creds
