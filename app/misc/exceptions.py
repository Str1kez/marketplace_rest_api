from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST


class CustomValidationError(HTTPException):
    def __init__(
            self,
            message: str | None = None,
            headers: str | None = None,
    ) -> None:
        self.status_code = HTTP_400_BAD_REQUEST
        if message:
            message = {'code': self.status_code,
                       'message': message}
        super().__init__(self.status_code, message, headers)
