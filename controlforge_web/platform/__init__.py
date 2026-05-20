from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for
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

from controlforge_web.auth.security import (
    get_locked_accounts,
    unlock_account
)

from flask_login import current_user

from controlforge.audit.platform_audit_logger import (
    write_platform_audit_event
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

@platform_bp.route(
    "/locked-accounts",
    methods=["GET", "POST"]
)
@login_required
@roles_required(["Manager"])
def locked_accounts():

    if request.method == "POST":

        username = request.form.get(
            "username"
        )

        unlock_account(
            username
        )

        write_platform_audit_event(
            action="account_unlocked",
            performed_by=current_user.username,
            details={
                "unlocked_account": username
            }
        )

        return redirect(
            url_for(
                "platform.locked_accounts"
            )
        )

    locked_accounts_list = (
        get_locked_accounts()
    )

    return render_template(
        "locked_accounts.html",
        locked_accounts=locked_accounts_list
    )