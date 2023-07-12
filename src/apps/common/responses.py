from rest_framework.response import Response


class ErrorResponse(Response):
    def __init__(self, message: str, status: int, **kwargs):
        kwargs["data"] = {"message": message}
        super().__init__(status=status, **kwargs)
