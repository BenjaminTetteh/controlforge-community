def analyze_risk_themes(
    findings: list
):

    themes = {
        "identity_and_access_management": 0,
        "segregation_of_duties": 0,
        "change_management": 0,
        "privileged_access": 0,
        "operations_and_monitoring": 0
    }

    for finding in findings:

        text = (
            f"{finding.get('control_name', '')} "
            f"{finding.get('issue_description', '')}"
        ).lower()

        if any(keyword in text for keyword in [
            "mfa",
            "access",
            "identity",
            "inactive",
            "dormant",
            "account"
        ]):
            themes[
                "identity_and_access_management"
            ] += 1

        if any(keyword in text for keyword in [
            "sod",
            "segregation"
        ]):
            themes[
                "segregation_of_duties"
            ] += 1

        if any(keyword in text for keyword in [
            "change",
            "deployment",
            "production"
        ]):
            themes[
                "change_management"
            ] += 1

        if any(keyword in text for keyword in [
            "privileged",
            "admin",
            "administrator"
        ]):
            themes[
                "privileged_access"
            ] += 1

        if any(keyword in text for keyword in [
            "monitoring",
            "logging",
            "alerting"
        ]):
            themes[
                "operations_and_monitoring"
            ] += 1

    return themes


def determine_dominant_themes(
    themes: dict,
    top_n: int = 3
):

    sorted_themes = sorted(
        themes.items(),
        key=lambda x: x[1],
        reverse=True
    )

    dominant = []

    for theme, count in sorted_themes:

        if count <= 0:
            continue

        readable_theme = (
            theme
            .replace("_", " ")
        )

        readable_theme = (
            readable_theme.capitalize()
        )

        dominant.append(
            {
                "theme": readable_theme,
                "count": count
            }
        )

    return dominant[:top_n]