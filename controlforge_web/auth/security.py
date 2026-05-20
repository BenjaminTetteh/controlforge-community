from controlforge_web.database import (
    get_db_connection
)


MAX_FAILED_ATTEMPTS = 5


def increment_failed_attempt(username):

    connection = get_db_connection()

    existing = connection.execute(
        """
        SELECT failed_attempts
        FROM failed_login_attempts
        WHERE username = ?
        """,
        (username,)
    ).fetchone()

    if existing:

        new_count = (
            existing["failed_attempts"]
            + 1
        )

        connection.execute(
            """
            UPDATE failed_login_attempts
            SET failed_attempts = ?
            WHERE username = ?
            """,
            (
                new_count,
                username
            )
        )

    else:

        new_count = 1

        connection.execute(
            """
            INSERT INTO failed_login_attempts (
                username,
                failed_attempts
            )
            VALUES (?, ?)
            """,
            (
                username,
                new_count
            )
        )

    connection.commit()

    connection.close()

    return new_count


def reset_failed_attempts(username):

    connection = get_db_connection()

    connection.execute(
        """
        DELETE FROM failed_login_attempts
        WHERE username = ?
        """,
        (username,)
    )

    connection.commit()

    connection.close()


def is_account_locked(username):

    connection = get_db_connection()

    row = connection.execute(
        """
        SELECT failed_attempts
        FROM failed_login_attempts
        WHERE username = ?
        """,
        (username,)
    ).fetchone()

    connection.close()

    if not row:
        return False

    return (
        row["failed_attempts"]
        >= MAX_FAILED_ATTEMPTS
    )


def get_locked_accounts():

    connection = get_db_connection()

    rows = connection.execute(
        """
        SELECT
            username,
            failed_attempts
        FROM failed_login_attempts
        WHERE failed_attempts >= ?
        """,
        (MAX_FAILED_ATTEMPTS,)
    ).fetchall()

    connection.close()

    return [
        {
            "username": row["username"],
            "failed_attempts": row["failed_attempts"]
        }
        for row in rows
    ]


def unlock_account(username):

    reset_failed_attempts(
        username
    )