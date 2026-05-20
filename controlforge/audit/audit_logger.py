import json
from datetime import datetime

from controlforge_web.database import (
    get_db_connection
)


def write_audit_event(
    engagement_path,
    action: str,
    performed_by: str,
    details: dict
):

    client_slug = engagement_path.parts[-2]
    engagement_slug = engagement_path.parts[-1]

    connection = get_db_connection()

    connection.execute(
        """
        INSERT INTO engagement_audit_events (
            client_slug,
            engagement_slug,
            timestamp,
            action,
            performed_by,
            details
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            client_slug,
            engagement_slug,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            action,
            performed_by,
            json.dumps(details)
        )
    )

    connection.commit()
    connection.close()