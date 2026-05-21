from pathlib import Path


EVIDENCE_ROOT = Path(
    "evidence"
)


def get_engagement_evidence_path(
    client_slug: str,
    engagement_slug: str
):

    path = (
        EVIDENCE_ROOT
        / client_slug
        / engagement_slug
    )

    path.mkdir(
        parents=True,
        exist_ok=True
    )

    return path