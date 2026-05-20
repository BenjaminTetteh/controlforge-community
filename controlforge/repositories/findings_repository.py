import json

from controlforge_web.database import (
    get_db_connection
)


def load_findings_for_engagement(
    client_slug: str,
    engagement_slug: str
):

    connection = get_db_connection()

    rows = connection.execute(
        """
        SELECT
            finding_id,
            severity,
            control_name,
            affected_user,
            source_system,
            status,
            remediation_owner,
            issue_description,
            raw_details
        FROM findings
        WHERE client_slug = ?
        AND engagement_slug = ?
        ORDER BY finding_id
        """,
        (
            client_slug,
            engagement_slug
        )
    ).fetchall()

    connection.close()

    findings = []

    for row in rows:

        raw_details = json.loads(
            row["raw_details"]
        )

        raw_details.update(
            {
                "finding_id": row["finding_id"],
                "severity": row["severity"],
                "control_name": row["control_name"],
                "affected_user": row["affected_user"],
                "source_system": row["source_system"],
                "status": row["status"],
                "remediation_owner": row["remediation_owner"],
                "issue_description": row["issue_description"]
            }
        )

        findings.append(
            raw_details
        )

    return findings


def update_finding_status(
    client_slug: str,
    engagement_slug: str,
    finding_id: str,
    new_status: str
):

    connection = get_db_connection()

    connection.execute(
        """
        UPDATE findings
        SET status = ?
        WHERE client_slug = ?
        AND engagement_slug = ?
        AND finding_id = ?
        """,
        (
            new_status,
            client_slug,
            engagement_slug,
            finding_id
        )
    )

    connection.commit()

    connection.close()