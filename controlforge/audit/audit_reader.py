import json


def load_audit_events(audit_file):

    if not audit_file.exists():
        return []

    events = []

    with open(audit_file, "r") as file:

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