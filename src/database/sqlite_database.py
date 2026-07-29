import sqlite3
from pathlib import Path
from sqlite3 import Connection, Cursor

from src.config.paths import DATABASE_FILE
from src.database.schema import (
    SCHEMA_VERSION_TABLE,
    EMAILS_TABLE,
    EMAILS_UNIQUE_INDEX,
    EMAILS_RECEIVED_INDEX,
    EMAILS_PROCESSING_INDEX,
)

class SQLiteDatabase:
    """
    Manages the application's SQLite database.
    
    Responsibilities:
        - Open and close the databse connection.
        - Configure the database schema.
        - Create the database schema.
        - Execute SQL statements.
        - Manage transactions.

    This class intentionally knows nothing about the domain
    (Email, Rules, Notifications, AI, etc)
    """

    @property
    def database_file(self) -> Path:
        return self._database_file

    @property
    def connection(self) -> Connection:
        if self._connection is None:
            raise RuntimeError(
                "Database has not been initialized."
            )

        return self._connection
    

    def __init__(
        self,
        database_file: str | Path = DATABASE_FILE,
    ) -> None:
        self._database_file = Path(database_file)
        self._connection: Connection | None = None

    # -----------------------------------------------------------
    # Lifecycle
    # -----------------------------------------------------------
    
    def initialize(self) -> None:
        """
        Initialize the database.
        """

        if self._connection is not None:
            return

        if self._database_file != Path(":memory:"):
            self._database_file.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

        try:
            self._connection = sqlite3.connect(self.database_file)
            self._connection.row_factory = sqlite3.Row
            self._configure()
            self._create_schema()
        except Exception:
            if self._connection is not None:
                self.connection.close()
                self._connection = None

            raise
        
    
    def close(self) -> None:
        """
        Close the database connection.
        """

        if self._connection is not None:
            self.connection.close()
            self._connection = None


    def table_exists(
        self,
        table_name: str,
    ) -> bool:

        row = self.fetchone(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
                AND name = ?;
            """,
            (table_name,),
        )

        return row is not None


    def index_exists(
        self,
        index_name: str,
    ) -> bool:

        row = self.fetchone(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'index'
                AND name = ?;
            """,
            (index_name,),
        )

        return row is not None


    # -----------------------------------------------------------
    # SQL
    # -----------------------------------------------------------
    
    def execute(
        self,
        query: str,
        parameters: tuple = (),
        *,
        commit: bool = True,
    ) -> Cursor:
        
        cursor = self.connection.execute(
            query,
            parameters,
        )

        if commit:
            self.commit()

        return cursor
    

    def executemany(
        self,
        query: str,
        parameters: list[tuple],
        *,
        commit: bool = True,
    ) -> Cursor:
        
        cursor = self.connection.executemany(
            query,
            parameters,
        )

        if commit:
            self.commit()

        return cursor

    
    def fetchone(
        self,
        query: str,
        parameters: tuple = (),
    ) -> sqlite3.Row | None:
        
        cursor = self.execute(
            query,
            parameters,
        )

        return cursor.fetchone()
    

    def fetchall(
        self,
        query: str,
        parameters: tuple = (),
    ) -> list[sqlite3.Row]:
        
        cursor = self.execute(
            query,
            parameters,
        )

        return cursor.fetchall()


    def commit(self) -> None:
        """
        Commit the current transaction.
        """

        self.connection.commit()


    def rollback(self) -> None:
        """
        Roll back the current transaction.
        """

        self.connection.rollback()

    # -----------------------------------------------------------
    # Context Manager
    # -----------------------------------------------------------
    
    def __enter__(self):

        self.initialize()
        return self
    
    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> bool:
        self.close()
        return False

    # -----------------------------------------------------------
    # Private
    # -----------------------------------------------------------
    
    def _configure(self) -> None:
        """
        Configure SQLite
        """

        self.execute(
            "PRAGMA foreign_keys = ON;"
        )

        self.execute(
            "PRAGMA journal_mode = WAL;"
        )

    def _create_schema(self) -> None:
        """
        Create the database schema
        """

        self.execute(SCHEMA_VERSION_TABLE)

        self.execute(EMAILS_TABLE)

        self.execute(EMAILS_UNIQUE_INDEX)

        self.execute(EMAILS_RECEIVED_INDEX)

        self.execute(EMAILS_PROCESSING_INDEX)