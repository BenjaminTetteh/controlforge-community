FINDING_STATUSES = [
    "Open",
    "Awaiting Remediation",
    "Remediation Submitted",
    "Under Auditor Review",
    "Closed",
    "Rejected"
]


ALLOWED_TRANSITIONS = {
    "Open": [
        "Awaiting Remediation"
    ],
    "Awaiting Remediation": [
        "Remediation Submitted"
    ],
    "Remediation Submitted": [
        "Under Auditor Review"
    ],
    "Under Auditor Review": [
        "Closed",
        "Rejected"
    ],
    "Rejected": [
        "Awaiting Remediation"
    ],
    "Closed": []
}


def is_valid_transition(
    current_status: str,
    new_status: str
):

    allowed_next_statuses = ALLOWED_TRANSITIONS.get(
        current_status,
        []
    )

    return new_status in allowed_next_statuses