import re
from pathlib import Path
from flask import (
    Blueprint,
    abort,
    flash,
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
from flask_login import current_user
from controlforge.repositories.findings_repository import (
    load_findings_for_engagement,
    update_finding_assignments,
    update_finding_status as update_finding_status_record
)
from controlforge.evidence.upload_service import (
    process_evidence_upload
)
from controlforge.governance.workflow import (
    FINDING_STATUSES,
    is_valid_transition
)
from controlforge.repositories.evidence_query_repository import (
    load_evidence_for_finding
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

    evidence_files = load_evidence_for_finding(
        finding_id=finding_id
    )

    finding = get_finding_or_404(
        findings,
        finding_id
    )

    return render_template(
        "finding_detail.html",
        finding=finding,
        allowed_statuses=FINDING_STATUSES,
        evidence_files=evidence_files
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

    remediation_owner = (
        finding.get(
            "remediation_owner"
        ) or ""
    ).strip()

    assigned_auditor = (
        finding.get(
            "assigned_auditor"
        ) or ""
    ).strip()

    closure_approver = (
        finding.get(
            "closure_approver"
        ) or ""
    ).strip()   

    new_status = request.form.get(
        "status"
    )

    if new_status not in FINDING_STATUSES:

        abort(400)

    old_status = finding.get(
        "status"
    )

    if (
        old_status == "Awaiting Remediation"
        and new_status == "Remediation Submitted"
    ):

        if current_user.username != remediation_owner:
            abort(403)


    if (
        old_status == "Remediation Submitted"
        and new_status == "Under Auditor Review"
    ):

        if current_user.username != assigned_auditor:
            abort(403)


    if (
        old_status == "Under Auditor Review"
        and new_status == "Rejected"
    ):

        if current_user.username != assigned_auditor:
            abort(403)


    if (
        old_status == "Under Auditor Review"
        and new_status == "Closed"
    ):

        allowed_closer = (
            current_user.username == closure_approver
            or current_user.role == "Manager"
        )

        if not allowed_closer:
            abort(403)

    if not is_valid_transition(
        old_status,
        new_status
    ):

        flash(
            f"Invalid workflow transition: "
            f"{old_status} → {new_status}"
        )

        return redirect(
            url_for(
                "findings.finding_detail",
                client_slug=client_slug,
                engagement_slug=engagement_slug,
                finding_id=finding_id
            )
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

@findings_bp.route(
    "/<client_slug>/<engagement_slug>/<finding_id>/upload-evidence",
    methods=["POST"]
)
@login_required
@roles_required(["Auditor", "Manager"])
def upload_evidence(
    client_slug,
    engagement_slug,
    finding_id
):

    findings = load_findings_for_engagement(
        client_slug=client_slug,
        engagement_slug=engagement_slug
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

    remediation_owner = (
        finding.get(
            "remediation_owner"
        ) or ""
    ).strip()

    if (
        remediation_owner
        != current_user.username
    ):

        abort(403)

    uploaded_files = request.files.getlist(
        "evidence_files"
    )

    if not uploaded_files:

        flash(
            "No files uploaded."
        )

        return redirect(
            url_for(
                "findings.finding_detail",
                client_slug=client_slug,
                engagement_slug=engagement_slug,
                finding_id=finding_id
            )
        )

    max_files = 5

    if len(uploaded_files) > max_files:

        flash(
            "You can upload a maximum of 5 files at a time."
        )

        return redirect(
            url_for(
                "findings.finding_detail",
                client_slug=client_slug,
                engagement_slug=engagement_slug,
                finding_id=finding_id
            )
        )

    uploaded_count = 0

    for uploaded_file in uploaded_files:

        success, message = process_evidence_upload(
            uploaded_file=uploaded_file,
            client_slug=client_slug,
            engagement_slug=engagement_slug,
            finding_id=finding_id,
            uploaded_by=current_user.username
        )

        if success:

            uploaded_count += 1

            write_audit_event(
                engagement_path=(
                    Path("clients")
                    / client_slug
                    / engagement_slug
                ),
                action="upload_evidence",
                performed_by=current_user.username,
                details={
                    "finding_id": finding_id,
                    "filename": uploaded_file.filename
                }
            )

        else:

            flash(
                message
            )

    flash(
        f"{uploaded_count} evidence file(s) uploaded successfully."
    )

    return redirect(
        url_for(
            "findings.finding_detail",
            client_slug=client_slug,
            engagement_slug=engagement_slug,
            finding_id=finding_id
        )
    )


@findings_bp.route(
    "/<client_slug>/<engagement_slug>/<finding_id>/assign",
    methods=["POST"]
)
@login_required
@roles_required(["Manager"])
def assign_finding_roles(
    client_slug,
    engagement_slug,
    finding_id
):

    remediation_owner = request.form.get(
        "remediation_owner",
        ""
    ).strip()

    assigned_auditor = request.form.get(
        "assigned_auditor",
        ""
    ).strip()

    closure_approver = request.form.get(
        "closure_approver",
        ""
    ).strip()

    update_finding_assignments(
        client_slug=client_slug,
        engagement_slug=engagement_slug,
        finding_id=finding_id,
        remediation_owner=remediation_owner,
        assigned_auditor=assigned_auditor,
        closure_approver=closure_approver
    )

    write_audit_event(
        engagement_path=(
            Path("clients")
            / client_slug
            / engagement_slug
        ),
        action="update_finding_assignments",
        performed_by=current_user.username,
        details={
            "finding_id": finding_id,
            "remediation_owner": remediation_owner,
            "assigned_auditor": assigned_auditor,
            "closure_approver": closure_approver
        }
    )

    flash(
        "Finding assignments updated successfully."
    )

    return redirect(
        url_for(
            "findings.finding_detail",
            client_slug=client_slug,
            engagement_slug=engagement_slug,
            finding_id=finding_id
        )
    )