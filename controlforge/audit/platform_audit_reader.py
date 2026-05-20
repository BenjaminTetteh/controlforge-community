import json

from controlforge_web.database import (
    get_db_connection
)


def load_platform_audit_events():

    connection = get_db_connection()

    rows = connection.execute(
        """
        SELECT
            id,
            timestamp,
            action,
            performed_by,
            details
        FROM platform_audit_events
        ORDER BY id DESC
        LIMIT 100
        """
    ).fetchall()

    connection.close()

    events = []

    for row in rows:

        events.append(
            {
                "id": row["id"],
                "timestamp": row["timestamp"],
                "action": row["action"],
                "performed_by": row["performed_by"],
                "details": json.loads(
                    row["details"]
                )
            }
        )

    return events