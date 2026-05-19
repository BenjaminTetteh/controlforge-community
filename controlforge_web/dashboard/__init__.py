import re

from flask import Blueprint, abort, render_template, request

from controlforge_web.services.dashboard_service import (
    build_dashboard_context
)

from controlforge.context.engagement_discovery import (
    discover_engagements
)

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/dashboard"
)

SEVERITY_RANK = {
    "Critical": 4,
    "High": 3,
    "Medium": 2,
    "Low": 1
}

def is_safe_slug(value: str) -> bool:

    return bool(
        re.fullmatch(
            r"[a-z0-9-]+",
            value
        )
    )


def get_posture_class(posture):

    if posture == "Strong":
        return "kpi-strong"

    if posture in ["Moderate", "Satisfactory"]:
        return "kpi-moderate"

    return "kpi-risk"


def get_trend_class(trend):

    if trend == "Improving":
        return "kpi-strong"

    if trend == "Stable":
        return "kpi-moderate"

    return "kpi-risk"


@dashboard_bp.route("/")
def engagement_list():

    engagements = discover_engagements()

    return render_template(
        "engagements.html",
        engagements=engagements
    )


@dashboard_bp.route(
    "/<client_slug>/<engagement_slug>"
)
def engagement_dashboard(
    client_slug,
    engagement_slug
):

    if (
        not is_safe_slug(client_slug)
        or not is_safe_slug(engagement_slug)
    ):
        abort(400)

    dashboard_context = build_dashboard_context(
        client_slug=client_slug,
        engagement_slug=engagement_slug
    )

    severity_filter = request.args.get("severity")
    owner_filter = request.args.get("owner")
    search_query = request.args.get(
        "search",
        ""
    ).strip()
    findings = dashboard_context["findings"]

    if severity_filter:
        findings = [
            finding
            for finding in findings
            if finding.get("severity") == severity_filter
        ]

    if owner_filter:

        findings = [
            finding
            for finding in findings
            if finding.get(
                "remediation_owner"
            ) == owner_filter
        ]

    if search_query:

        query = search_query.lower()

        findings = [
            finding
            for finding in findings
            if (
                query in finding.get(
                    "finding_id",
                    ""
                ).lower()

                or query in finding.get(
                    "affected_user",
                    ""
                ).lower()

                or query in finding.get(
                    "control_name",
                    ""
                ).lower()

                or query in finding.get(
                    "remediation_owner",
                    ""
                ).lower()
            )
        ]

    sort_by = request.args.get(
        "sort",
        "severity_desc"
    )    

    if sort_by == "severity_asc":

        findings = sorted(
            findings,
            key=lambda finding: SEVERITY_RANK.get(
                finding.get("severity"),
                0
            )
        )

    elif sort_by == "owner":

        findings = sorted(
            findings,
            key=lambda finding: finding.get(
                "remediation_owner",
                ""
            )
        )

    elif sort_by == "status":

        findings = sorted(
            findings,
            key=lambda finding: finding.get(
                "status",
                ""
            )
        )

    elif sort_by == "finding_id":

        findings = sorted(
            findings,
            key=lambda finding: finding.get(
                "finding_id",
                ""
            )
        )

    else:

        findings = sorted(
            findings,
            key=lambda finding: SEVERITY_RANK.get(
                finding.get("severity"),
                0
            ),
            reverse=True
        )

    per_page = 10

    total_findings = len(findings)

    page = request.args.get(
        "page",
        1,
        type=int
    )

    start = (
        page - 1
    ) * per_page

    end = start + per_page

    paginated_findings = findings[
        start:end
    ]

    total_pages = (
        total_findings + per_page - 1
    ) // per_page



    kpis = dashboard_context["kpis"]

    kpi_classes = {
        "governance_posture": get_posture_class(
            kpis["governance_posture"]
        ),
        "governance_trend": get_trend_class(
            kpis["governance_trend"]
        )
    }

    return render_template(
        "dashboard.html",
        kpis=kpis,
        engagement=dashboard_context["engagement"],
        concentrations=dashboard_context["concentrations"],
        findings=paginated_findings,
        page=page,
        total_pages=total_pages,
        search_query=search_query,
        selected_severity=severity_filter,
        kpi_classes=kpi_classes,
        charts=dashboard_context["charts"],
        remediation_metrics=dashboard_context["remediation_metrics"],
        owner_summary=dashboard_context["owner_summary"],
        selected_owner=owner_filter,
        owners=sorted(
            set(
                finding.get(
                    "remediation_owner",
                    "Unassigned"
                )
                for finding in dashboard_context["findings"]
            )
        ),
        selected_sort=sort_by,
        audit_events=dashboard_context["audit_events"],
    )