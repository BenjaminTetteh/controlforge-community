from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for
)

from flask_login import (
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

            login_user(
                user
            )

            return redirect(
                url_for(
                    "dashboard.engagement_list"
                )
            )

        write_platform_audit_event(
            action="login_failure",
            performed_by=username or "unknown",
            details={
                "reason": "invalid_credentials"
            }
        )

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
def logout():

    write_platform_audit_event(
        action="logout",
        performed_by=current_user.username,
        details={
            "role": current_user.role
        }
    )

    logout_user()

    return redirect(
        url_for(
            "auth.login"
        )
    )