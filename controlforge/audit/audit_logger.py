import json
from datetime import datetime


def write_audit_event(
    engagement_path,
    action: str,
    performed_by: str,
    details: dict
):

    audit_dir = engagement_path / "audit_logs"

    audit_dir.mkdir(
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