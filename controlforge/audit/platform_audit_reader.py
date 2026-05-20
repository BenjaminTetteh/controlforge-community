import json
from pathlib import Path


PLATFORM_AUDIT_FILE = (
    Path("controlforge_web")
    / "data"
    / "platform_audit_logs"
    / "events.jsonl"
)


def load_platform_audit_events():

    if not PLATFORM_AUDIT_FILE.exists():
        return []

    events = []

    with open(
        PLATFORM_AUDIT_FILE,
        "r"
    ) as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            events.append(
                json.loads(line)
            )

    return list(
        reversed(events)
    )