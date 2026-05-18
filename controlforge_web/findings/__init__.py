import re
from pathlib import Path

from flask import Blueprint, abort, render_template

from controlforge.analytics.findings_loader import (
    load_saved_findings
)


findings_bp = Blueprint(
    "findings",
    __name__,
    url_prefix="/findings"
)


def is_safe_slug(value: str) -> bool:
    return bool(
        re.fullmatch(
            r"[a-z0-9-]+",
            value
        )
    )


def is_safe_finding_id(value: str) -> bool:
    return bool(
        re.fullmatch(
            r"[A-Z0-9-]+",
            value
        )
    )


@findings_bp.route(
    "/<client_slug>/<engagement_slug>/<finding_id>"
)
def finding_detail(
    client_slug,
    engagement_slug,
    finding_id
):

    if (
        not is_safe_slug(client_slug)
        or not is_safe_slug(engagement_slug)
        or not is_safe_finding_id(finding_id)
    ):
        abort(400)

    engagement_path = (
        Path("clients")
        / client_slug
        / engagement_slug
    )

    if not engagement_path.exists():
        abort(404)

    findings = load_saved_findings(
        engagement_path / "findings"
    )

    finding = next(
        (
            item
            for item in findings
            if item["finding_id"] == finding_id
        ),
        None
    )

    if not finding:
        abort(404)

    return render_template(
        "finding_detail.html",
        finding=finding
    )