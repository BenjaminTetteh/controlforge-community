from pathlib import Path

from controlforge.analytics.findings_loader import (
    load_saved_findings
)

from controlforge.context.engagement_loader import (
    load_engagement_context
)

from controlforge.frameworks.governance_kpi_generator import (
    generate_governance_kpis
)

from controlforge.frameworks.governance_scorecard import (
    generate_governance_scorecard
)

from controlforge.frameworks.risk_concentration_analyzer import (
    analyze_risk_concentration
)

from controlforge.reports.chart_renderer import (
    generate_findings_severity_chart
)

from controlforge.reports.governance_heatmap import (
    generate_governance_heatmap
)


def build_dashboard_context(
    client_slug,
    engagement_slug
):

    engagement_path = (
        Path("clients")
        / client_slug
        / engagement_slug
    )

    findings_path = (
        engagement_path
        / "findings"
    )

    engagement_context = (
        load_engagement_context(
            engagement_path
        )
    )

    findings = load_saved_findings(
        findings_path
    )

    open_findings = len([
        finding
        for finding in findings
        if finding.get("status") == "Open"
    ])

    closed_findings = len([
        finding
        for finding in findings
        if finding.get("status") == "Closed"
    ])

    overdue_findings = len([
        finding
        for finding in findings
        if finding.get("status") == "Overdue"
    ])

    remediation_completion = 0

    if findings:

        remediation_completion = round(
            (
                closed_findings
                / len(findings)
            ) * 100
        )

    scorecard = generate_governance_scorecard(
        framework_code="SOX",
        engagement_path=engagement_path,
        findings=findings
    )

    concentrations = analyze_risk_concentration(
        findings
    )

    charts_path = (
        Path("controlforge_web")
        / "static"
        / "generated"
    )

    severity_chart = generate_findings_severity_chart(
        metrics=scorecard,
        output_path=charts_path
    )

    heatmap_chart = generate_governance_heatmap(
        concentrations=concentrations,
        output_dir=charts_path / "charts"
    )

    trends = {
        "coverage_trend": "Stable",
        "critical_findings_trend": "Stable",
        "open_findings_trend": "Stable"
    }

    kpis = generate_governance_kpis(
        scorecard=scorecard,
        concentrations=concentrations,
        trends=trends
    )

    return {
        "engagement": engagement_context,
        "kpis": kpis,
        "concentrations": concentrations,
        "findings": findings,
        "charts": {
            "severity_chart": "generated/charts/findings_by_severity.png",
            "heatmap_chart": "generated/charts/governance_heatmap.png"
        },
        "remediation_metrics": {
            "open": open_findings,
            "closed": closed_findings,
            "overdue": overdue_findings,
            "completion": remediation_completion
        }
    }