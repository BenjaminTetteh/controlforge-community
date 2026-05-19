import json
from pathlib import Path

from werkzeug.security import generate_password_hash


users = [
    {
        "id": "1",
        "username": "auditor",
        "password": "auditor123",
        "role": "Auditor"
    },
    {
        "id": "2",
        "username": "manager",
        "password": "manager123",
        "role": "Manager"
    },
    {
        "id": "3",
        "username": "viewer",
        "password": "viewer123",
        "role": "Viewer"
    }
]


output_file = (
    Path("controlforge_web")
    / "data"
    / "users.json"
)


secure_users = []

for user in users:

    secure_users.append(
        {
            "id": user["id"],
            "username": user["username"],
            "password_hash": generate_password_hash(
                user["password"]
            ),
            "role": user["role"]
        }
    )


with open(output_file, "w") as file:
    json.dump(
        secure_users,
        file,
        indent=2
    )


print("Demo users created successfully.")