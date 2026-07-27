from dataclasses import dataclass
from datetime import datetime

@dataclass(slots=True)
class Email:
    """
    Domain model representing an email optained from a provider.

    This model intentionally contains only provider-derived
    information and has no persistence concerns.
    """

    provider: str
    provider_message_id: str
    thread_id: str
    
    sender: str
    recipients_to: str
    recipients_cc: str
    recipients_bcc: str
    reply_to: str

    subject: str
    body_text: str
    body_html: str | None
    
    received_on: datetime | None
    