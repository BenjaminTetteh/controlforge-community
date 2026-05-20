from flask import (
    Blueprint,
    render_template
)

from flask_login import (
    login_required
)

from controlforge.audit.platform_audit_reader import (
    load_platform_audit_events
)

from controlforge_web.auth.permissions import (
    roles_required
)


platform_bp = Blueprint(
    "platform",
    __name__,
    url_prefix="/platform"
)


@platform_bp.route(
    "/security-activity"
)
@login_required
@roles_required(["Manager"])
def security_activity():

    events = load_platform_audit_events()

    return render_template(
        "platform_security_activity.html",
        events=events[:100]
    )