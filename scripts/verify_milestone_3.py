"""
Milestone 3 verification
"""

from src.application import verify_project_structure
from src.database.sqlite_database import SQLiteDatabase
from src.repositories.email_repository import EmailRepository
from src.database import queries

from datetime import UTC, datetime
from src.constants.processing_status import ProcessingStatus
from src.models.email import Email
from src.models.email_record import EmailRecord
from src.repositories import exceptions

import uuid

def verify(
    condition: bool,
    description: str,
) -> None:

    if condition:
        print(f"[PASS] {description}")
    else:
        raise RuntimeError(
            f"[FAIL] {description}"
        )

print("=" * 60)
print("Email Monitor - Milestone 3 Verification")
print("=" * 60)
print()

print("Project Verification")
print("-" * 60)

verify(
    queries.EMAIL_INSERT != "",
    "queries.py",
)

verify_project_structure()
print("[PASS] Project Structure")


print()
print("Repository Verification")
print("-" * 60)

database = SQLiteDatabase(":memory:")
database.initialize()
print("[PASS] Database Initialized")

repository = EmailRepository(database)

verify(
    repository is not None,
    "EmailRepository construction",
)

verify(
    repository.exists(
        provider="gmail",
        provider_message_id="MSG-001",
    ) is False,
    "EmailRepository.exists()"
)

timestamp = repository._now()

verify(
    timestamp.tzinfo is not None,
    "EmailRepository._now()",
)


message_id = str(uuid.uuid4())
email = Email(
    provider = "gmail",
    provider_message_id = message_id,
    thread_id = "THREAD-001",
    sender="john@example.com",
    recipients_to="alice@example.com",
    recipients_cc = "",
    recipients_bcc = "",
    reply_to = "john@example.com",
    subject = "Test Email",
    body_text = "Hello World",
    body_html = "<p>Hello World</p>",
    received_on = datetime.now(UTC),
)
now = repository._now()
record = EmailRecord(
    id = None,
    email = email,
    processing_status = ProcessingStatus.NEW,
    last_error = None,
    created_on = now,
    updated_on = now,
)
parameters = repository._record_to_parameters(record)
verify(
    len(parameters) == 16,
    "EmailRepository._record_to_parameters()",
)

now = repository._now()

row = {
    "id": 1,
    "provider": "gmail",
    "provider_message_id": "MSG-001",
    "thread_id": "THREAD-001",
    "sender": "john@example.com",
    "recipients_to": "alice@example.com",
    "recipients_cc": "",
    "recipients_bcc": "",
    "reply_to": "john@example.com",
    "subject": "Repository Test",
    "body_text": "Hello World",
    "body_html": "<p>Hello World</p>",
    "received_on": now.isoformat(),
    "processing_status": ProcessingStatus.NEW.value,
    "last_error": None,
    "created_on": now.isoformat(),
    "updated_on": now.isoformat(),
}

mapped_record = repository._row_to_record(row)

verify(
    mapped_record.id == 1,
    "EmailRepository._row_to_record(): id",
)

verify(
    mapped_record.email.provider == "gmail",
    "EmailRepository._row_to_record(): provider",
)

verify(
    mapped_record.email.provider_message_id == "MSG-001",
    "EmailRepository._row_to_record(): provider_message_id",
)

verify(
    mapped_record.processing_status == ProcessingStatus.NEW,
    "EmailRepository._row_to_record(): processing_status",
)

verify(
    mapped_record.last_error is None,
    "EmailRepository._row_to_record(): last_error",
)

verify(
    mapped_record.created_on == now,
    "EmailRepository._row_to_record(): created_on",
)

verify(
    mapped_record.updated_on == now,
    "EmailRepository._row_to_record(): updated_on",
)


print()
print("Public API Verification")
print("-" * 60)


record_id = repository.save(record)

verify(
    record_id > 0,
    "EmailRepository.save()",
)


duplicate_record = EmailRecord(
    id = None,
    email = email,
    processing_status = ProcessingStatus.NEW,
    last_error = None,
    created_on = repository._now(),
    updated_on = repository._now(),
)

try:
    repository.save(duplicate_record)
    raise RuntimeError(
        "Expected DuplicateEmailError"
    )
except exceptions.DuplicateEmailError:
    verify(
        True,
        "DuplicateEmailError",
    )


record = repository.get_by_id(record_id)

verify(
    record is not None,
    "EmailRepository.get_by_id()",
)

verify(
    record.id == record_id,
    "Retrieved record ID",
)

record = repository.get_by_provider_message_id(
    provider = "gmail",
    provider_message_id = message_id,
)

verify(
    record is not None,
    "EmailRepository.get_by_provider_message_id()"
)

verify(
    record.email.provider_message_id == message_id,
    "Provider message ID matches",
)

record = repository.update_status(
    record_id,
    ProcessingStatus.SUMMARIZED,
)

verify(
    record.processing_status == ProcessingStatus.SUMMARIZED,
    "EmailRepository.update_status()",
)

verify(
    record.last_error is None,
    "Last error cleared",
)

record = repository.update_failure(
    record_id,
    "Verification Failure",
)

verify(
    record.processing_status == ProcessingStatus.FAILED,
    "EmailRepository.update_failure()",
)

verify(
    record.last_error == "Verification Failure",
    "Failure message stored",
)

verify(
    repository.delete(record_id),
    "EmailRepository.delete()"
)

verify(
    repository.get_by_id(record_id) is None,
    "Deleted record cannot be retrieved",
)

verify(
    repository.exists(
        provider = "gmail",
        provider_message_id = message_id,
    ) is False,
    "Deleted record no longer exists",
)

print()
print("=" * 60)
print("Milestone 3 Verification Successful")
print("=" * 60)

database.close()