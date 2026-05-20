import sqlite3
from pathlib import Path


DATABASE_PATH = (
    Path("controlforge_web")
    / "data"
    / "controlforge.db"
)


def get_db_connection():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():

    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS failed_login_attempts (
            username TEXT PRIMARY KEY,
            failed_attempts INTEGER NOT NULL
        )
        """
    )

    connection.commit()

    connection.close()