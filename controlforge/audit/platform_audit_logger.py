import json
from datetime import datetime
from pathlib import Path


def write_platform_audit_event(
    action: str,
    performed_by: str,
    details: dict
):

    audit_dir = (
        Path("controlforge_web")
        / "data"
        / "platform_audit_logs"
    )

    audit_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    audit_file = audit_dir / "events.jsonl"

    event = {
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "action": action,
        "performed_by": performed_by,
        "details": details
    }

    with open(audit_file, "a") as file:
        file.write(
            json.dumps(event)
            + "\n"
        )

    return event