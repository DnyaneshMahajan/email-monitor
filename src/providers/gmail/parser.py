from src.models.email import Email
from src.utils.datetime import parse_email_datetime
from src.utils.text import clean_text

class GmailParser:
    """
    Converts Gmail API responses into Email domain objects.
    """
    
    @staticmethod
    def parse(message: dict) -> Email:
        
        headers = {
            header["name"]: header["value"]
            for header in message["payload"]["headers"]
        }

        sender = clean_text(headers.get("From"))
        subject = clean_text(headers.get("Subject"))
        snippet = clean_text(message.get("snippet"))

        received_on = parse_email_datetime(headers.get("Date"))

        return Email(
            provider_message_id = message["id"],
            thread_id = message["threadId"],
            sender = sender,
            subject = subject,
            snippet = snippet,
            received_on = received_on
        )
    