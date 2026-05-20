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

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS platform_audit_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            action TEXT NOT NULL,
            performed_by TEXT NOT NULL,
            details TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS engagement_audit_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_slug TEXT NOT NULL,
            engagement_slug TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            action TEXT NOT NULL,
            performed_by TEXT NOT NULL,
            details TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS findings (
            finding_id TEXT PRIMARY KEY,
            client_slug TEXT NOT NULL,
            engagement_slug TEXT NOT NULL,
            severity TEXT NOT NULL,
            control_name TEXT,
            affected_user TEXT,
            source_system TEXT,
            status TEXT,
            remediation_owner TEXT,
            issue_description TEXT,
            raw_details TEXT
        )
        """
    )

    connection.commit()

    connection.close()