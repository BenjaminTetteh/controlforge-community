import json
from pathlib import Path


TRACKER_FILE = (
    Path("controlforge_web")
    / "data"
    / "security"
    / "failed_login_tracker.json"
)


MAX_FAILED_ATTEMPTS = 5


def load_failed_attempts():

    if not TRACKER_FILE.exists():
        return {}

    with open(TRACKER_FILE, "r") as file:
        return json.load(file)


def save_failed_attempts(data):

    with open(TRACKER_FILE, "w") as file:
        json.dump(
            data,
            file,
            indent=2
        )


def increment_failed_attempt(username):

    data = load_failed_attempts()

    current = data.get(
        username,
        0
    )

    data[username] = current + 1

    save_failed_attempts(
        data
    )

    return data[username]


def reset_failed_attempts(username):

    data = load_failed_attempts()

    if username in data:
        del data[username]

    save_failed_attempts(
        data
    )


def is_account_locked(username):

    data = load_failed_attempts()

    attempts = data.get(
        username,
        0
    )

    return attempts >= MAX_FAILED_ATTEMPTS


def get_locked_accounts():

    data = load_failed_attempts()

    return [
        {
            "username": username,
            "failed_attempts": attempts
        }
        for username, attempts in data.items()
        if attempts >= MAX_FAILED_ATTEMPTS
    ]


def unlock_account(username):

    data = load_failed_attempts()

    if username in data:
        del data[username]

    save_failed_attempts(
        data
    )