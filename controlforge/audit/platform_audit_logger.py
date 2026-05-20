import json
from datetime import datetime

from controlforge_web.database import (
    get_db_connection
)


def write_platform_audit_event(
    action: str,
    performed_by: str,
    details: dict
):

    connection = get_db_connection()

    connection.execute(
        """
        INSERT INTO platform_audit_events (
            timestamp,
            action,
            performed_by,
            details
        )
        VALUES (?, ?, ?, ?)
        """,
        (
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