import pytest
from django.core.handlers.wsgi import WSGIRequest
from faker import Faker

from apps.users.models import LoginInProgress
from meme_wars.tests.test_case import TestCase


class TestLoginInProgress(TestCase):
    def test_should_add_login_in_progress_data_to_session(self):
        request = self.get_request_example()
        login_success_redirect_url = Faker().url()
        login_failure_redirect_url = Faker().url()
        LoginInProgress.add_to_session(
            request=request,
            login_success_redirect_url=login_success_redirect_url,
            login_failure_redirect_url=login_failure_redirect_url,
        )
        login_in_progress_dict = request.session[LoginInProgress.session_key]
        self.assertIsInstance(login_in_progress_dict["google_auth_state"], str)
        self.assertEqual(login_in_progress_dict["login_success_redirect_url"], login_success_redirect_url)
        self.assertEqual(login_in_progress_dict["login_failure_redirect_url"], login_failure_redirect_url)

    def test_should_should_raise_key_error_when_session_does_not_contain_required_data(self):
        request = self.get_request_example()
        self.assertNotIn(LoginInProgress.session_key, request.session)
        with pytest.raises(expected_exception=KeyError, match="'login_in_progress'"):
            LoginInProgress(request=request)

        login_in_progress_data = _create_required_login_in_progress()
        login_in_progress_data.pop("login_failure_redirect_url")
        request.session[LoginInProgress.session_key] = login_in_progress_data
        with pytest.raises(expected_exception=KeyError, match="'login_failure_redirect_url'"):
            LoginInProgress(request=request)

        login_in_progress_data = _create_required_login_in_progress()
        login_in_progress_data.pop("login_success_redirect_url")
        request.session[LoginInProgress.session_key] = login_in_progress_data
        with pytest.raises(expected_exception=KeyError, match="'login_success_redirect_url'"):
            LoginInProgress(request=request)

        login_in_progress_data = _create_required_login_in_progress()
        login_in_progress_data.pop("google_auth_state")
        request.session[LoginInProgress.session_key] = login_in_progress_data
        with pytest.raises(expected_exception=KeyError, match="'google_auth_state'"):
            LoginInProgress(request=request)

    def test_should_create_login_in_progress_from_session_data_and_clear_that_session_data(self):
        request = self._add_login_in_progress_data_to_session()
        login_in_progress = LoginInProgress(request=request)
        session_data = request.session[LoginInProgress.session_key]
        self.assertEqual(login_in_progress.google_auth_state, session_data["google_auth_state"])
        self.assertEqual(login_in_progress.login_success_redirect_url, session_data["login_success_redirect_url"])
        self.assertEqual(login_in_progress.login_failure_redirect_url, session_data["login_failure_redirect_url"])

    def test_should_clear_that_session_data(self):
        request = self._add_login_in_progress_data_to_session()
        self.assertIn(LoginInProgress.session_key, request.session)
        LoginInProgress.clear_from_session(request=request)
        self.assertNotIn(LoginInProgress.session_key, request.session)

    def _add_login_in_progress_data_to_session(self) -> WSGIRequest:
        request = self.get_request_example()
        request.session[LoginInProgress.session_key] = _create_required_login_in_progress()
        return request


def _create_required_login_in_progress() -> dict:
    return {
        "google_auth_state": "google-auth-state",
        "login_success_redirect_url": Faker().url(),
        "login_failure_redirect_url": Faker().url(),
    }
