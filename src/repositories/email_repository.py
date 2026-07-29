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

    # CREATE
    def save(
        self,
        record: EmailRecord,
    ) -> int:
        """
        Save a new email record

        Returns:
            The database ID of the newly inserted record.
        """

        if record.id is not None:
            ValueError(
                "Cannot save an EmailRecord that already has an ID. Use update_status() instead."
            )

        return self._insert(record)


    # READ
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
        record_id: int,
    ) -> EmailRecord | None:
        """
        Retrieve an email record by its database ID.

        Returns:
            EmailRecord if found, otherwise None.
        """

        row = self._database.fetchone(
            queries.EMAIL_SELECT_BY_ID,
            (record_id,),
        )

        if row is None:
            return None

        return self._row_to_record(row)


    def get_by_provider_message_id(
        self,
        provider: str,
        provider_message_id: str,
    ) -> EmailRecord | None:
        """
        Retrieve an email record using the provider and provider message ID.
        
        Returns:
            EmailRecord if found, otherwise None.
        """

        row = self._database.fetchone(
            queries.EMAIL_SELECT_BY_PROVIDER_MESSAGE_ID,
            (
                provider,
                provider_message_id,
            ),
        )

        if row is None:
            return None

        return self._row_to_record(row)
    

    # UPDATE
    def update_status(
        self,
        record_id: int,
        status: ProcessingStatus,
        last_error: str | None = None,
    ) -> EmailRecord:
        """
        Update the processing status of an email
        
        Returns:
            The updated EmailRecord.
            
        Raises:
            RepositoryError:
                If the email record does not exist.
        """
        updated_on = self._now()

        cursor = self._database.execute(
            queries.EMAIL_UPDATE_STATUS,
            (
                status,
                last_error,
                updated_on,
                record_id,
            )
        )

        if cursor.rowcount == 0:
            raise exceptions.RepositoryError(
                f"Email record with ID {record_id}, does not exist."
            )

        record = self.get_by_id(record_id)

        if record is None:
            raise EmailRepository(
                f"Failed to retrieve updated email record with ID {record_id}."
            )
        
        return record


    def update_failure(
            self,
            record_id: int,
            error: str,
    ) -> EmailRecord:
        """
        Mark an email as failed and record the error message.
        
        Returns:
            The updated EmailRecord.
        """

        return self.update_status(
            record_id = record_id,
            status = ProcessingStatus.FAILED,
            last_error = error,
        )


    # DELETE
    def delete(
        self,
        record_id: int,
    ) -> bool:
        """
        Delete an email record.
        
        Returns:
            True if the record was deleted, otherwise False.
        """

        cursor = self._database.execute(
            queries.EMAIL_DELETE_BY_ID,
            (record_id,),
        )

        return cursor.rowcount > 0

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