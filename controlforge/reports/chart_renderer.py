from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


def generate_findings_severity_chart(
    metrics: dict,
    output_path
):

    labels = [
        "Critical",
        "High",
        "Medium",
        "Low"
    ]

    values = [
        metrics.get("critical_findings", 0),
        metrics.get("high_findings", 0),
        metrics.get("medium_findings", 0),
        metrics.get("low_findings", 0)
    ]

    charts_dir = output_path / "charts"

    charts_dir.mkdir(
        exist_ok=True
    )

    chart_file = (
        charts_dir
        / "findings_by_severity.png"
    )

    plt.figure(figsize=(8, 5))

    bars = plt.bar(
        labels,
        values
    )

    plt.title(
        "Findings by Severity"
    )

    plt.xlabel(
        "Severity"
    )

    plt.ylabel(
        "Number of Findings"
    )

    for bar in bars:

        height = bar.get_height()

        plt.text(
            bar.get_x()
            + bar.get_width() / 2,
            height,
            str(height),
            ha="center",
            va="bottom"
        )

    plt.tight_layout()

    plt.savefig(chart_file)

    plt.close()

    print("\nChart generated:")
    print(f"- {chart_file}")

    return chart_file