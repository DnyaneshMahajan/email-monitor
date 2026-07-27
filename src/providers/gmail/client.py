from googleapiclient.discovery import build
from src.providers.gmail.auth import get_credentials

class GmailClient:
    def __init__(self):
        self.service = build(
            "gmail",
            "v1",
            credentials=get_credentials()
        )
    
    def list_latest_messages(self, count: int = 10):

        response = (
            self.service.users()
            .messages()
            .list(
                userId="me",
                maxResults=count,
            )
            .execute()
        )

        return response.get("messages", [])
    
    def get_message(self, message_id: str):
        return (
            self.service.users()
            .messages()
            .get(
                userId="me",
                id=message_id,
            )
            .execute()
        )
    
