import http
import os
import traceback
from unittest.mock import MagicMock, patch

import pytest

from aws.api.v1.src.lambdas.hello_lambda.app import (
    generate_response,
    greet_user,
    handle_exception,
    lambda_handler,
    logger,
    validate_input,
)
from utils.errors import InvalidQueryStringParameterError, MissingRequiredQueryStringParameterError

app_module = "aws.api.v1.src.lambdas.hello_lambda.app"


@pytest.fixture
def mock_env():
    """Mock environment setup."""
    with patch.dict(os.environ, {"DOCS_DOMAIN_NAME": "example.com"}):
        yield


@pytest.fixture
def mock_context():
    """Creates a mock context object."""
    return MagicMock()


@pytest.mark.unit
@pytest.mark.usefixtures("mock_env")
@pytest.mark.parametrize(
    "event, expected",
    [
        ({"queryStringParameters": {"name": "Test"}}, "Test"),
        (
            {"queryStringParameters": {}},
            MissingRequiredQueryStringParameterError("'name' query string parameter is required"),
        ),
        (
            {"queryStringParameters": {"name": ""}},
            InvalidQueryStringParameterError("Invalid name provided"),
        ),
        (
            {"queryStringParameters": {"name": None}},
            InvalidQueryStringParameterError("Invalid name provided"),
        ),
        (
            {"queryStringParameters": {"name": "  "}},
            InvalidQueryStringParameterError("Invalid name provided"),
        ),
    ],
)
def test_validate_input(event, expected):
    """Validate input function tests."""
    if isinstance(expected, str):
        assert validate_input(event) == expected
    else:
        with pytest.raises(expected.__class__) as e:
            validate_input(event)
        assert str(e.value) == str(expected)


@pytest.mark.unit
def test_greet_user():
    """Greet user returns expected message when given valid name."""
    assert greet_user("Test") == {"message": "Hello, Test!"}


@pytest.mark.unit
@pytest.mark.usefixtures("mock_env")
def test_generate_response():
    """Generate response returns expected response when given valid body."""
    response = generate_response({"message": "Hello, Test!"})
    assert response["statusCode"] == http.HTTPStatus.OK
    assert response["headers"]["Content-Type"] == "application/json"
    assert response["headers"]["Access-Control-Allow-Origin"] == "https://example.com"
    assert response["headers"]["Access-Control-Allow-Methods"] == "OPTIONS,GET,POST,PUT,DELETE"
    assert response["body"] == '{"message": "Hello, Test!"}'


@pytest.mark.unit
@pytest.mark.usefixtures("mock_env", "mock_context")
@pytest.mark.parametrize("event", [({"queryStringParameters": {"name": "Test"}})])
@patch(f"{app_module}.validate_input", return_value="Test")
@patch(f"{app_module}.greet_user", return_value={"message": "Hello, Test!"})
@patch(f"{app_module}.generate_response", return_value="response")
def test_lambda_handler_valid_response(
    mock_validate_input, mock_greet_user, mock_generate_response, event, mock_context
):
    """Lambda handler returns expected response when given valid event."""
    response = lambda_handler(event, mock_context)
    assert response == "response"
    mock_validate_input.assert_called_once()
    mock_greet_user.assert_called_once()
    mock_generate_response.assert_called_once()


@pytest.mark.unit
@pytest.mark.usefixtures("mock_env", "mock_context")
@pytest.mark.parametrize(
    "event, side_effect",
    [
        (
            {"queryStringParameters": {}},
            MissingRequiredQueryStringParameterError("'name' query string parameter is required"),
        ),
        (
            {"queryStringParameters": {"name": ""}},
            InvalidQueryStringParameterError("Invalid name provided"),
        ),
        (
            {"queryStringParameters": {"name": None}},
            InvalidQueryStringParameterError("Invalid name provided"),
        ),
        (
            {"queryStringParameters": {"name": "  "}},
            InvalidQueryStringParameterError("Invalid name provided"),
        ),
    ],
)
def test_lambda_handler_error_response(event, side_effect, mock_context):
    """Lambda handler returns error response when given invalid event."""
    with patch(
        f"{app_module}.validate_input", side_effect=side_effect
    ) as mock_validate_input, patch(
        f"{app_module}.handle_exception", return_value="error_response"
    ) as mock_handle_exception:
        response = lambda_handler(event, mock_context)

        assert response == "error_response"
        mock_validate_input.assert_called_once()
        mock_handle_exception.assert_called_once()


@pytest.mark.unit
@pytest.mark.usefixtures("mock_env")
@pytest.mark.parametrize(
    "exception, status",
    [
        (
            InvalidQueryStringParameterError("Invalid name provided"),
            http.HTTPStatus.BAD_REQUEST,
        ),
        (
            MissingRequiredQueryStringParameterError("'name' query string parameter is required"),
            http.HTTPStatus.BAD_REQUEST,
        ),
        (
            Exception("An error occurred processing your request."),
            http.HTTPStatus.INTERNAL_SERVER_ERROR,
        ),
    ],
)
def test_handle_exception(mock_env, exception, status):
    """Handle exception correctly logs and returns response for given exception."""

    expected_response = generate_response({"error": str(exception)}, status)

    with patch.object(logger, "error") as mock_log:
        response = handle_exception(exception)
        mock_log.assert_called_with({"error": str(exception), "trace": traceback.format_exc()})
        assert response == expected_response
