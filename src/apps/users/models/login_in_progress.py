import hashlib
import os

from django.core.handlers.wsgi import WSGIRequest


class LoginInProgress:
    session_key = "login_in_progress"

    def __init__(self, request: WSGIRequest):
        data = request.session[self.session_key]
        self.google_auth_state = data["google_auth_state"]
        self.login_success_redirect_url = data["login_success_redirect_url"]
        self.login_failure_redirect_url = data["login_failure_redirect_url"]

    @classmethod
    def clear_from_session(cls, request: WSGIRequest) -> None:
        del request.session[cls.session_key]

    @classmethod
    def add_to_session(
        cls, request: WSGIRequest, login_success_redirect_url: str, login_failure_redirect_url: str
    ) -> None:
        request.session[cls.session_key] = {
            "google_auth_state": hashlib.sha256(os.urandom(1024)).hexdigest(),
            "login_success_redirect_url": login_success_redirect_url,
            "login_failure_redirect_url": login_failure_redirect_url,
        }
