from __future__ import annotations
from datetime import UTC, datetime

import sqlite3

from src.database.sqlite_database import SQLiteDatabase
from src.models.email import Email
from src.models.email_record import EmailRecord
from src.database import queries
from src.repositories import exceptions
from src.constants.processing_status import ProcessingStatus


class EmailRepository:
    """
    Repository responsible for persisting Email objects
    
    This class forms the boundary between the application's
    domain model and the persistence layer.
    """

    def __init__(
        self,
        database: SQLiteDatabase,
    ) -> None:
        """
        Initialize the repository
        
        Args:
            database:
                Initialized SQLite database
        """

        self._database = database

    #
    # Public API
    #

    def save(
        self,
        email: Email,
    ) -> EmailRecord:
        raise NotImplementedError


    def exists(
        self,
        *,
        provider: str,
        provider_message_id: str,
    ) -> bool:
        """
        Determine whether an email already exists.
        
        Args:
            provider:
                Email provider.
                
            provider_message_id:
                Provider-specific message identifier.
                
        Returns:
            True if the email exists.
            False otherwise
        """

        row = self._database.fetchone(
            queries.EMAIL_EXISTS,
            (
                provider,
                provider_message_id,
            ),
        )

        return row is not None


    def get_by_id(
        self,
        id: int,
    ) -> EmailRecord | None:
        raise NotImplementedError


    def get_by_provider_message_id(
        self,
        provider: str,
        provider_message_id: str,
    ) -> EmailRecord | None:
        raise NotImplementedError


    def update(
        self,
        record: EmailRecord,
    ) -> None:
        raise NotImplementedError


    def delete(
        self,
        id: int,
    ) -> None:
        raise NotImplementedError

    #
    # Private helpers
    #

    def _insert(
        self,
        record: EmailRecord,
    ) -> int:
        """
        Insert an email record into the database.
        
        Args:
            record:
                Email record to insert
                
        Returns:
            Generated database ID.
        """

        parameters = self._record_to_parameters(record)

        try:
            cursor = self._database.execute(
                queries.EMAIL_INSERT,
                parameters,
            )
            return int(cursor.lastrowid)
        
        except sqlite3.IntegrityError as ex:
            raise exceptions.DuplicateEmailError(
                "Email already exists"
            ) from ex
        except sqlite3.DatabaseError as ex:
            raise exceptions.EmailInsertError(
                "Unable to insert email."
            ) from ex
        
    
    def _row_to_record(
        self,
        row: sqlite3.Row,
    ) -> EmailRecord:
        """
        Convert a database row into an EmailRecord.
        
        Args:
            row:
                SQLite row.
                
        Returns:
            EmailRecord
        """

        email = Email(
            provider = row["provider"],
            provider_message_id = row["provider_message_id"],
            thread_id = row["thread_id"],
            sender = row["sender"],
            recipients_to = row["recipients_to"],
            recipients_cc = row["recipients_cc"],
            recipients_bcc = row["recipients_bcc"],
            reply_to = row["reply_to"],
            subject = row["subject"],
            body_text = row["body_text"],
            body_html = row["body_html"],
            received_on = self._parse_datetime(
                row["received_on"],
            ),
        )

        return EmailRecord(
            id = row["id"],
            email = email,
            processing_status = ProcessingStatus(
                row["processing_status"],
            ),
            last_error = row["last_error"],
            created_on = self._parse_datetime(
                row["created_on"],
            ),
            updated_on = self._parse_datetime(
                row["updated_on"],
            ),
        )

    def _record_to_parameters(
        self,
        record: EmailRecord,
    ) -> tuple[Any, ...]:
        """
        Convert an EmailRecord into SQL parameters.
        
        Args:
            record:
                Email record to persist.
                
        Returns:
            SQL parameter tuple.
        """
        email = record.email

        return (
            email.provider,
            email.provider_message_id,
            email.thread_id,
            email.sender,
            email.recipients_to,
            email.recipients_cc,
            email.recipients_bcc,
            email.reply_to,
            email.subject,
            email.body_text,
            email.body_html,
            email.received_on.isoformat()
            if email.received_on is not None
            else None,
            record.processing_status.value,
            record.last_error,
            record.created_on.isoformat(),
            record.updated_on.isoformat(),
        )
    

    def _now(
        self,
    ) -> datetime:
        """
        Return the current UTC timestamp.
        
        Returns:
            Current UTC timestamp.
        """

        return datetime.now(UTC)


    def _parse_datetime(
        self,
        value: str | None,
    ) -> datetime | None:
        """
        Parse an ISO-8601 timestamp
        
        Args:
            value:
                ISO-8601 timestamp
                
        Returns:
            Parsed datetime or None.
        """

        if value is None:
            return None

        return datetime.fromisoformat(value)