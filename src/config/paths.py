from pathlib import Path

# ==============================================================
# Project directories
# ==============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SRC_DIR = PROJECT_ROOT / "src"
CONFIG_DIR = SRC_DIR / "config"
PROVIDERS_DIR = SRC_DIR / "providers"

DATA_DIR = PROJECT_ROOT / "data"
LOG_DIR = PROJECT_ROOT / "logs"
TESTS_DIR = PROJECT_ROOT / "tests"
CREDENTIALS_DIR = PROJECT_ROOT / "credentials"

# ==============================================================
# Files
# ==============================================================

DATABASE_FILE = DATA_DIR / "email_monitor.db"

CREDENTIALS_FILE = CREDENTIALS_DIR / "credentials.json"
TOKEN_FILE = CREDENTIALS_DIR / "token.json"

def verify_project_structure() -> None:
    """
    Verify and prepare the project runtime environment.
    
    Responsibilities:
        - Create application-managed directories if they do not exist."
        - Verify user-provided resource exist.
        - Fail fast with meaningful error messages.
    """

    # Create application-managed directories
    for directory in (
        DATA_DIR,
        LOG_DIR,
    ):
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )    

        if not directory.is_dir():
            raise NotADirectoryError(
                f"{directory} is not a directory."
            )

    # Verify credentials directory
    if not CREDENTIALS_DIR.exists():
        raise FileNotFoundError(
            f"Credentials directory not found:\n"
            f"{CREDENTIALS_DIR}"
        )

    if not CREDENTIALS_DIR.is_dir():
        raise NotADirectoryError(
            f"{CREDENTIALS_DIR} is not a directory."
        )
    
    # Verify OAuth credentials file
    if not CREDENTIALS_FILE.exists():
        raise FileNotFoundError(
            f"Gmail OAuth credentials file not found:\n"
            f" {CREDENTIALS_FILE}\n\n"
            f"Download 'credentials.json from Google Cloud Console "
            f"and place it in the credentials directory"
        )

    if not CREDENTIALS_FILE.is_file():
        raise FileNotFoundError(
            f"{CREDENTIALS_FILE} is not a file."
        )