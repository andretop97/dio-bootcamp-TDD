class BaseException(Exception):
    message: str = "Internal server Erro"

    def __init__(self, message: str | None = None) -> None:
        if message:
            self.message = message


class NotFoundException(BaseException):
    message = "Not found"


class ValidationErrorException(BaseException):
    message = "Validation error"
