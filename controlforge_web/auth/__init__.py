from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for
)

from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from werkzeug.security import (
    check_password_hash
)

from controlforge_web.auth.user import (
    get_user_by_username
)

from controlforge.audit.audit_logger import (
    write_audit_event
)

from controlforge.audit.platform_audit_logger import (
    write_platform_audit_event
)

from flask_login import current_user

from controlforge_web.auth.security import (
    increment_failed_attempt,
    is_account_locked,
    reset_failed_attempts
)

from flask import session


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


@auth_bp.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    error = None

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        if is_account_locked(username):

            write_platform_audit_event(
                action="login_blocked_account_locked",
                performed_by=username,
                details={
                    "reason": "too_many_failed_attempts"
                }
            )

            error = "Account is locked due to too many failed login attempts."

            return render_template(
                "login.html",
                error=error
            )

        password = request.form.get(
            "password"
        )

        user = get_user_by_username(
            username
        )

        if (
            user
            and check_password_hash(
                user.password_hash,
                password
            )
        ):
            write_platform_audit_event(
                action="login_success",
                performed_by=username,
                details={
                    "role": user.role
                }
            )

            reset_failed_attempts(
                username
            )

            session.permanent = True

            login_user(
                user
            )

            return redirect(
                url_for(
                    "dashboard.engagement_list"
                )
            )

        failed_attempts = increment_failed_attempt(
            username
        )

        write_platform_audit_event(
            action="login_failure",
            performed_by=username or "unknown",
            details={
                "reason": "invalid_credentials",
                "failed_attempts": failed_attempts
            }
        )

        error = "Invalid username or password."

        error = (
            "Invalid username or password."
        )

    return render_template(
        "login.html",
        error=error
    )


@auth_bp.route(
    "/logout"
)
@login_required
def logout():

    username = current_user.username
    role = current_user.role

    write_platform_audit_event(
        action="logout",
        performed_by=username,
        details={
            "role": role
        }
    )

    logout_user()

    return redirect(
        url_for(
            "auth.login"
        )
    )