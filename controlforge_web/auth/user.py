import json
from pathlib import Path

from flask_login import UserMixin


USERS_FILE = (
    Path("controlforge_web")
    / "data"
    / "users.json"
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


def load_users():

    if not USERS_FILE.exists():
        return []

    with open(USERS_FILE, "r") as file:
        data = json.load(file)

    return [
        User(
            user_data["id"],
            user_data["username"],
            user_data["password_hash"],
            user_data["role"]
        )
        for user_data in data
    ]


def get_user_by_id(user_id):

    users = load_users()

    for user in users:

        if user.id == user_id:
            return user

    return None


def get_user_by_username(username):

    users = load_users()

    for user in users:

        if user.username == username:
            return user

    return None