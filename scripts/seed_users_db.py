import json
from pathlib import Path

from controlforge_web.database import (
    get_db_connection
)


USERS_FILE = (
    Path("controlforge_web")
    / "data"
    / "users.json"
)


def load_users():

    with open(USERS_FILE, "r") as file:
        return json.load(file)


def seed_users():

    users = load_users()

    connection = get_db_connection()

    cursor = connection.cursor()

    for user in users:

        cursor.execute(
            """
            INSERT OR REPLACE INTO users (
                id,
                username,
                password_hash,
                role
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                user["id"],
                user["username"],
                user["password_hash"],
                user["role"]
            )
        )

    connection.commit()

    connection.close()

    print(
        "Users seeded successfully."
    )


if __name__ == "__main__":
    seed_users()