from src.database.sqlite_database import SQLiteDatabase

def main() -> None:
    
    database = SQLiteDatabase()
    
    database.initialize()
    print("SQLite initialized successfully.")

    database.close()
    print("SQLite closed successfully.")


if __name__ == "__main__":
    main()