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

from controlforge_web.auth.user import (
    DEMO_USERS
)


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

    if request.method == "POST":

        username = request.form.get(
            "username"
        )

        user = DEMO_USERS.get(
            username
        )

        if user:
            login_user(
                user
            )

            return redirect(
                url_for(
                    "dashboard.engagement_list"
                )
            )

    return render_template(
        "login.html"
    )


@auth_bp.route(
    "/logout"
)
def logout():

    logout_user()

    return redirect(
        url_for(
            "auth.login"
        )
    )