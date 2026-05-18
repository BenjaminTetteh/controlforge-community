from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


def generate_governance_heatmap(
    concentrations: list,
    output_dir
):

    if not concentrations:
        return None

    domains = [
        item["domain"]
        for item in concentrations
    ]

    scores = []

    for item in concentrations:

        risk_level = item["risk_level"]

        if risk_level == "Critical Risk":
            scores.append(4)

        elif risk_level == "High Risk":
            scores.append(3)

        elif risk_level == "Moderate Risk":
            scores.append(2)

        else:
            scores.append(1)

    fig, ax = plt.subplots(
        figsize=(10, 4)
    )

    heatmap = ax.imshow(
        [scores],
        aspect="auto",
        cmap="RdYlGn_r",
        vmin=1,
        vmax=4
    )

    ax.set_xticks(
        range(len(domains))
    )

    ax.set_xticklabels(
        domains,
        rotation=15,
        ha="right"
    )

    ax.set_yticks([])

    plt.colorbar(
        heatmap,
        label="Risk Intensity"
    )

    plt.title(
        "Governance Risk Heatmap"
    )

    output_dir = Path(output_dir)

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        output_dir
        / "governance_heatmap.png"
    )

    plt.tight_layout()

    plt.savefig(output_file)

    plt.close()

    return output_file