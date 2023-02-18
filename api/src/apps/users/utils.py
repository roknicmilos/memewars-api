from apps.users.authentication import GoogleUser
from apps.users.models import User


def get_or_create_user(google_user: GoogleUser) -> tuple[User, bool]:
    defaults = {
        'first_name': google_user.given_name,
        'last_name': google_user.family_name,
        'image_url': google_user.picture,
    }
    user, is_created = User.objects.get_or_create(email=google_user.email, defaults=defaults)
    if not is_created:
        user.update(**defaults)
    return user, is_created
