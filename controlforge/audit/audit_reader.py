import json

from controlforge_web.database import (
    get_db_connection
)


def load_audit_events(
    client_slug,
    engagement_slug
):

    connection = get_db_connection()

    rows = connection.execute(
        """
        SELECT
            id,
            timestamp,
            action,
            performed_by,
            details
        FROM engagement_audit_events
        WHERE client_slug = ?
        AND engagement_slug = ?
        ORDER BY id DESC
        LIMIT 100
        """,
        (
            client_slug,
            engagement_slug
        )
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