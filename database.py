
import sqlite3
from pathlib import Path


# Get the main project directory
BASE_DIR = Path(__file__).resolve().parent

# Database location
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "calcmaster.db"


def get_connection():
    """Create and return a connection to the SQLite database."""

    # Create the data folder if it does not exist
    DATA_DIR.mkdir(exist_ok=True)

    # Connect to the database
    connection = sqlite3.connect(DATABASE_PATH)

    # Return database rows as dictionary-like objects
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    """Create the database tables if they do not already exist."""

    connection = get_connection()

    try:
        cursor = connection.cursor()

        # Table 1: Calculation history
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS calculation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operation TEXT NOT NULL,
                expression TEXT NOT NULL,
                result TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Table 2: Saved calculations
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS saved_calculations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                expression TEXT NOT NULL,
                result TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.commit()

    finally:
        connection.close()
