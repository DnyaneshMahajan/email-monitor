from datetime import datetime
from email.utils import parsedate_to_datetime

def parse_email_datetime(value: str | None) -> datetime | None:
    """
    Convert an RFC2822 email date into a datetime object.
    """

    if not value:
        return None
    
    try:
        return parsedate_to_datetime(value)
    except Exception:
        return None


def format_datetime(
        value: datetime | None,
) -> str:
    """
    Format datetime for console output.
    """

    if value is None:
        return ""
    
    return value.strftime("%d-%b-%Y %I:%M:%S %p")