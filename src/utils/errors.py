from flask import abort, Response
from json import dumps
from http import HTTPStatus

class ApiError(Exception):
    """Base error class"""

    def __init__(self, status_code, message):
        super(ApiError, self).__init__()
        self.status_code = status_code
        self.message = message
        self._exec()
    
    def _exec(self):
        abort(
            Response(
                response=dumps({'error': self.message}), 
                status=self.status_code)
            )


class BadRequestError(ApiError):
    """Bad request"""
    def __init__(self, message):
        super(BadRequestError, self).__init__(HTTPStatus.BAD_REQUEST, message)


class ConflictError(ApiError):
    """Conflict error"""

    def __init__(self, message):
        super(ConflictError, self).__init__(
            HTTPStatus.CONFLICT, message
        )


class UnauthorizedError(ApiError):
    """Unauthorized error"""

    def __init__(self, message):
        super(UnauthorizedError, self).__init__(
            HTTPStatus.UNAUTHORIZED, message
        )


class AccessDeniedError(ApiError):
    """Access denied error"""

    def __init__(self, message="Access denied"):
        super(AccessDeniedError, self).__init__(
            HTTPStatus.FORBIDDEN, message
        )


class UnprocessableEntityError(ApiError):
    """Unprocessable entity error"""

    def __init__(self, message):
        super(UnprocessableEntityError, self).__init__(
            HTTPStatus.UNPROCESSABLE_ENTITY, message
        )


class NotFoundError(ApiError):
    """Not Found entity error"""

    def __init__(self, message):
        super(NotFoundError, self).__init__(
            HTTPStatus.NOT_FOUND, message
        )

        