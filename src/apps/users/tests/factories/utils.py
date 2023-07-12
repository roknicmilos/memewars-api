from uuid import uuid4

from apps.users.authentication import GoogleUser
from apps.users.models import User


def build_email(user: User | GoogleUser) -> str:
    """
    Adds a unique string in the email making it sure it is unique
    """

    email_prefix = ""
    if isinstance(user, User):
        email_prefix = f"{user.first_name}.{user.last_name}"
    elif isinstance(user, GoogleUser):
        email_prefix = f"{user.given_name}.{user.family_name}"

    return f"{email_prefix}.{uuid4().hex}@example.rs"
