import http


class CustomError(Exception):
    """Base class for other custom exceptions."""

    status_code = http.HTTPStatus.INTERNAL_SERVER_ERROR


class BadRequestError(CustomError):
    """Custom error for bad requests (400)."""

    status_code = http.HTTPStatus.BAD_REQUEST


class MissingRequiredQueryStringParameterError(BadRequestError):
    """Raised when the required query string parameter is missing"""

    pass


class InvalidQueryStringParameterError(BadRequestError):
    """Raised when the query string parameter is invalid"""

    pass


class UnauthorizedError(CustomError):
    """Custom error for unauthorized requests (401)."""

    status_code = http.HTTPStatus.UNAUTHORIZED


class ForbiddenError(CustomError):
    """Custom error for forbidden requests (403)."""

    status_code = http.HTTPStatus.FORBIDDEN


class NotFoundError(CustomError):
    """Custom error for not found requests (404)."""

    status_code = http.HTTPStatus.NOT_FOUND


class InternalServerError(CustomError):
    """Custom error for internal server errors (500)."""

    status_code = http.HTTPStatus.INTERNAL_SERVER_ERROR


class NotImplementedError(CustomError):
    """Custom error for not implemented errors (501)."""

    status_code = http.HTTPStatus.NOT_IMPLEMENTED


class ServiceUnavailableError(CustomError):
    """Custom error for service unavailable errors (503)."""

    status_code = http.HTTPStatus.SERVICE_UNAVAILABLE


class GatewayTimeoutError(CustomError):
    """Custom error for gateway timeout errors (504)."""

    status_code = http.HTTPStatus.GATEWAY_TIMEOUT
