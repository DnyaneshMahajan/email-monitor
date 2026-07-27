from datetime import datetime

from src.application import verify_project_structure
from src.database.sqlite_database import SQLiteDatabase
from src.models.email import Email
from src.models.email_record import EmailRecord
from src.constants.processing_status import ProcessingStatus


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
print("Email Monitor - Milestone 2 Verification")
print("=" * 60)
print()

#
# Project Structure
#

verify_project_structure()
print("[PASS] Project Structure")

#
# Database
#

database = SQLiteDatabase()
database.initialize()
print("[PASS] Database Initialized")

#
# Tables
#

verify(
    database.table_exists("schema_version"),
    "schema_version table",
)

verify(
    database.table_exists("emails"),
    "emails table",
)

#
# Indexes
#

verify(
    database.index_exists("idx_emails_provider_message"),
    "provider_message index",
)

verify(
    database.index_exists("idx_emails_received_on"),
    "received_on index",
)

verify(
    database.index_exists("idx_emails_processing_status"),
    "processing_status index",
)

#
# Email model
#

email = Email(
    provider = "gmail",
    provider_message_id = "MSG-001",
    thread_id = "THREAD-001",
    sender = "john@example.com",
    recipients_to = "alice@example.com",
    recipients_cc = "",
    recipients_bcc = "",
    reply_to = "john@example.com",
    subject = "Test Email",
    body_text = "Hello World",
    body_html = "<p>Hello World</p>",
    received_on = datetime.now(),
)

verify(
    email.provider == "gmail",
    "Email model",
)

#
# EmailRecord model
#

record = EmailRecord(
    id = None,
    email = email,
    processing_status = ProcessingStatus.NEW,
    last_error = None,
    created_on = datetime.now(),
    updated_on = datetime.now(),
)

verify(
    record.processing_status == ProcessingStatus.NEW,
    "EmailRecord model",
)

#
# Enum
#

expected = {
    "NEW",
    "SUMMARIZED",
    "RULES_EVALUATED",
    "NOTIFIED",
    "FAILED",
}

actual = {status.value for status in ProcessingStatus}

verify(
    actual == expected,
    "ProcessingStatus enum",
)
database.close()

print()
print("=" * 60)
print("Milestone 2 Verification Successful")
print("=" * 60)