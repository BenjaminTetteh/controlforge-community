from flask_login import UserMixin

from controlforge_web.database import (
    get_db_connection
)


class User(UserMixin):

    def __init__(
        self,
        user_id,
        username,
        password_hash,
        role
    ):
        self.id = user_id
        self.username = username
        self.password_hash = password_hash
        self.role = role


def row_to_user(row):

    if row is None:
        return None

    return User(
        row["id"],
        row["username"],
        row["password_hash"],
        row["role"]
    )


def get_user_by_id(user_id):

    connection = get_db_connection()

    user_row = connection.execute(
        """
        SELECT
            id,
            username,
            password_hash,
            role
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    ).fetchone()

    connection.close()

    return row_to_user(
        user_row
    )


def get_user_by_username(username):

    connection = get_db_connection()

    user_row = connection.execute(
        """
        SELECT
            id,
            username,
            password_hash,
            role
        FROM users
        WHERE username = ?
        """,
        (username,)
    ).fetchone()

    connection.close()

    return row_to_user(
        user_row
    )