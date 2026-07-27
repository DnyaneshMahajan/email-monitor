from dataclasses import dataclass
from datetime import datetime
from src.models.email import Email
from src.constants.processing_status import ProcessingStatus

@dataclass(slots=True)
class EmailRecord:
    """
    Represents a persisted email in the application's database
    """

    id: int | None
    email: Email
    processing_status: ProcessingStatus
    last_error: str | None
    created_on: datetime
    updated_on: datetime
