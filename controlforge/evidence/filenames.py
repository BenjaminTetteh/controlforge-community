import secrets
from pathlib import Path


def generate_secure_filename(
    original_filename: str
):

    extension = Path(
        original_filename
    ).suffix.lower()

    random_name = secrets.token_hex(
        16
    )

    return (
        f"{random_name}{extension}"
    )