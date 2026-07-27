"""
Database schema definitions.
"""

SCHEMA_VERSION_TABLE = """
CREATE TABLE IF NOT EXISTS schema_version
(
    version INTEGER NOT NULL
);
"""

EMAILS_TABLE = """
CREATE TABLE IF NOT EXISTS emails
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider TEXT NOT NULL,
    provider_message_id TEXT NOT NULL,
    thread_id TEXT NOT NULL,
    sender TEXT NOT NULL,
    recipients_to TEXT NOT NULL,
    recipients_cc TEXT NOT NULL,
    recipients_bcc TEXT NOT NULL,
    reply_to TEXT NOT NULL,
    subject TEXT NOT NULL,
    body_text TEXT NOT NULL,
    body_html TEXT,
    received_on TEXT,
    processing_status TEXT NOT NULL,
    last_error TEXT,
    created_on TEXT NOT NULL,
    updated_on TEXT NOT NULL
);
"""

EMAILS_UNIQUE_INDEX = """
CREATE UNIQUE INDEX IF NOT EXISTS
idx_emails_provider_message
ON emails
(
    provider,
    provider_message_id
);
"""

EMAILS_RECEIVED_INDEX = """
CREATE INDEX IF NOT EXISTS
idx_emails_received_on
ON emails
(
    received_on
);
"""

EMAILS_PROCESSING_INDEX = """
CREATE INDEX IF NOT EXISTS
idx_emails_processing_status
on emails
(
    processing_status
);
"""
