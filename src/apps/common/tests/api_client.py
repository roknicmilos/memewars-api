import json as json_utils

from rest_framework.test import APIClient as BaseAPIClient


def _prepare_kwargs(func):
    def wrapper(*args, json=None, **kwargs):  # pragma: no cover
        if json:
            kwargs["data"] = json_utils.dumps(json)
            kwargs["content_type"] = "application/json"
        return func(*args, **kwargs)

    return wrapper


class APIClient(BaseAPIClient):
    @_prepare_kwargs
    def post(self, path: str, json: dict = None, **kwargs):
        return super().post(path, **kwargs)

    @_prepare_kwargs
    def put(self, path: str, json: dict = None, **kwargs):
        return super().put(path, **kwargs)

    @_prepare_kwargs
    def patch(self, path: str, json: dict = None, **kwargs):
        return super().patch(path, **kwargs)
