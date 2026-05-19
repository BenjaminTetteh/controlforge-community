from flask_login import UserMixin


class DemoUser(UserMixin):

    def __init__(
        self,
        user_id,
        username,
        role
    ):
        self.id = user_id
        self.username = username
        self.role = role


DEMO_USERS = {
    "auditor": DemoUser(
        "1",
        "auditor",
        "Auditor"
    ),
    "manager": DemoUser(
        "2",
        "manager",
        "Manager"
    ),
    "viewer": DemoUser(
        "3",
        "viewer",
        "Viewer"
    )
}


def get_user_by_id(user_id):

    for user in DEMO_USERS.values():

        if user.id == user_id:
            return user

    return None