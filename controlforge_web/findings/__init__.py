import re
from pathlib import Path

from flask import (
    Blueprint,
    abort,
    redirect,
    render_template,
    request,
    url_for
)

from controlforge.audit.audit_logger import (
    write_audit_event
)

from flask_login import login_required

from controlforge_web.auth.permissions import (
    roles_required
)

from controlforge.repositories.findings_repository import (
    update_finding_status as update_finding_status_record
)

from flask_login import current_user

from controlforge.repositories.findings_repository import (
    load_findings_for_engagement,
    update_finding_status as update_finding_status_record
)


findings_bp = Blueprint(
    "findings",
    __name__,
    url_prefix="/findings"
)


ALLOWED_STATUSES = [
    "Open",
    "In Progress",
    "Closed",
    "Overdue"
]


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


def get_engagement_path(
    client_slug: str,
    engagement_slug: str
):
    return (
        Path("clients")
        / client_slug
        / engagement_slug
    )


def validate_route_params(
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


def get_finding_or_404(
    findings,
    finding_id
):

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

    return finding


@findings_bp.route(
    "/<client_slug>/<engagement_slug>/<finding_id>"
)
@login_required
def finding_detail(
    client_slug,
    engagement_slug,
    finding_id
):

    validate_route_params(
        client_slug,
        engagement_slug,
        finding_id
    )

    engagement_path = get_engagement_path(
        client_slug,
        engagement_slug
    )

    if not engagement_path.exists():
        abort(404)

    findings = load_findings_for_engagement(
        client_slug=client_slug,
        engagement_slug=engagement_slug
    )

    finding = get_finding_or_404(
        findings,
        finding_id
    )

    return render_template(
        "finding_detail.html",
        finding=finding,
        allowed_statuses=ALLOWED_STATUSES
    )


@findings_bp.route(
    "/<client_slug>/<engagement_slug>/<finding_id>/status",
    methods=["POST"]
)
@login_required
@roles_required(["Auditor", "Manager"])
def update_finding_status(
    client_slug,
    engagement_slug,
    finding_id
):

    validate_route_params(
        client_slug,
        engagement_slug,
        finding_id
    )

    engagement_path = get_engagement_path(
        client_slug,
        engagement_slug
    )

    if not engagement_path.exists():
        abort(404)

    findings_path = (
        engagement_path
        / "findings"
    )

    findings = load_findings_for_engagement(
        client_slug=client_slug,
        engagement_slug=engagement_slug
    )

    finding = get_finding_or_404(
        findings,
        finding_id
    )

    new_status = request.form.get(
        "status"
    )

    if new_status not in ALLOWED_STATUSES:
        abort(400)

    old_status = finding.get(
        "status"
    )

    if old_status != new_status:

        update_finding_status_record(
            client_slug=client_slug,
            engagement_slug=engagement_slug,
            finding_id=finding_id,
            new_status=new_status
        )

        write_audit_event(
            engagement_path=engagement_path,
            action="update_finding_status",
            performed_by=current_user.username,
            details={
                "finding_id": finding_id,
                "old_status": old_status,
                "new_status": new_status
            }
        )

    return redirect(
        url_for(
            "findings.finding_detail",
            client_slug=client_slug,
            engagement_slug=engagement_slug,
            finding_id=finding_id
        )
    )