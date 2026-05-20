import json
from pathlib import Path

from controlforge.analytics.findings_loader import (
    load_saved_findings
)

from controlforge_web.database import (
    get_db_connection
)


CLIENT_SLUG = "meridian-financial-group"
ENGAGEMENT_SLUG = "2026-q2-sox-itgc"


def seed_findings():

    engagement_path = (
        Path("clients")
        / CLIENT_SLUG
        / ENGAGEMENT_SLUG
    )

    findings = load_saved_findings(
        engagement_path / "findings"
    )

    connection = get_db_connection()

    for finding in findings:

        connection.execute(
            """
            INSERT OR REPLACE INTO findings (
                finding_id,
                client_slug,
                engagement_slug,
                severity,
                control_name,
                affected_user,
                source_system,
                status,
                remediation_owner,
                issue_description,
                raw_details
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                finding.get("finding_id"),
                CLIENT_SLUG,
                ENGAGEMENT_SLUG,
                finding.get("severity"),
                finding.get("control_name"),
                finding.get("affected_user"),
                finding.get("source_system"),
                finding.get("status"),
                finding.get("remediation_owner"),
                finding.get("issue_description"),
                json.dumps(finding)
            )
        )

    connection.commit()
    connection.close()

    print("Findings seeded successfully.")


if __name__ == "__main__":
    seed_findings()