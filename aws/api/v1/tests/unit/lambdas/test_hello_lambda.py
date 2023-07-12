import http
import json
import os
import traceback
from unittest.mock import MagicMock, patch

import pytest
from api.v1.src.lambdas.hello_lambda.app import (
    InvalidNameError,
    generate_response,
    greet_user,
    handle_exception,
    lambda_handler,
    logger,
    validate_input,
)


@pytest.fixture
def valid_event():
    """Valid lambda event."""
    return {"queryStringParameters": {"name": "Test"}}


@pytest.fixture
def invalid_event():
    """Invalid lambda event."""
    return {"queryStringParameters": {}}


@pytest.fixture
def mock_env():
    """Mock environment setup."""
    with patch.dict(os.environ, {"DOCS_DOMAIN_NAME": "example.com"}):
        yield


@pytest.mark.unit
@pytest.mark.usefixtures("mock_env")
def test_validate_input_when_given_valid_event_returns_expected_name(
    valid_event,
):
    """Validate input returns expected name when given valid event."""
    assert validate_input(valid_event) == "Test"


@pytest.mark.unit
@pytest.mark.usefixtures("mock_env")
def test_validate_input_when_given_invalid_event_raises_InvalidNameError(
    invalid_event,
):
    """Validate input raises InvalidNameError when given invalid event."""
    with pytest.raises(InvalidNameError):
        validate_input(invalid_event)


@pytest.mark.unit
def test_greet_user_when_given_valid_name_returns_expected_message():
    """Greet user returns expected message when given valid name."""
    assert greet_user("Test") == {"message": "Hello, Test!"}


@pytest.mark.unit
@pytest.mark.usefixtures("mock_env")
def test_generate_response_when_given_valid_body_returns_expected_response():
    """Generate response returns expected response when given valid body."""
    response = generate_response({"message": "Hello, Test!"})
    assert response["statusCode"] == 200
    assert response["headers"]["Content-Type"] == "application/json"
    assert (
        response["headers"]["Access-Control-Allow-Origin"]
        == "https://example.com"
    )
    assert (
        response["headers"]["Access-Control-Allow-Methods"]
        == "OPTIONS,GET,POST,PUT,DELETE"
    )
    assert response["body"] == '{"message": "Hello, Test!"}'


@pytest.mark.unit
@pytest.mark.usefixtures("mock_env")
@patch(
    "api.v1.src.lambdas.hello_lambda.app.validate_input", return_value="Test"
)
@patch(
    "api.v1.src.lambdas.hello_lambda.app.greet_user",
    return_value={"message": "Hello, Test!"},
)
@patch(
    "api.v1.src.lambdas.hello_lambda.app.generate_response",
    return_value="response",
)
def test_lambda_handler_when_given_valid_event_returns_expected_response(
    mock_validate_input, mock_greet_user, mock_generate_response, valid_event
):
    """Lambda handler returns expected response when given valid event."""
    context = MagicMock()
    response = lambda_handler(valid_event, context)
    assert response == "response"
    mock_validate_input.assert_called_once()
    mock_greet_user.assert_called_once()
    mock_generate_response.assert_called_once()


@pytest.mark.unit
@pytest.mark.usefixtures("mock_env")
@patch(
    "api.v1.src.lambdas.hello_lambda.app.validate_input",
    side_effect=InvalidNameError("Invalid name provided"),
)
@patch(
    "api.v1.src.lambdas.hello_lambda.app.handle_exception",
    return_value="error_response",
)
def test_lambda_handler_when_given_invalid_event_returns_error_response(
    mock_validate_input, mock_handle_exception, invalid_event
):
    """Lambda handler returns error response when given invalid event."""
    context = MagicMock()
    response = lambda_handler(invalid_event, context)
    assert response == "error_response"
    mock_validate_input.assert_called_once()
    mock_handle_exception.assert_called_once()


@pytest.mark.unit
def test_lambda_handler_empty_name():
    # Arrange: Set up the event and context
    event = {"queryStringParameters": {"name": ""}}  # edge case: empty string
    context = MagicMock()

    # Act: Call the function with the edge case input
    response = lambda_handler(event, context)

    # Assert: Check the response to make sure the function behaved as expected
    assert response["statusCode"] == http.HTTPStatus.INTERNAL_SERVER_ERROR
    assert json.loads(response["body"])["message"] == "Invalid name provided"


@pytest.mark.unit
def test_handle_exception_for_invalid_name_error(mock_env):
    """Handle exception correctly logs and returns response for
    InvalidNameError."""

    # Setup: Create an exception
    exception = InvalidNameError("Invalid name provided")

    # Mock the logger
    with patch.object(logger, "error") as mock_log:
        # Act: Call the function with the exception
        response = handle_exception(exception)

        # Assert: Check that the logger was called with the correct arguments
        mock_log.assert_called_with(
            {"message": str(exception), "trace": traceback.format_exc()}
        )

        # Assert: Check that the function returned the correct response
        assert response == generate_response(
            {"message": str(exception)}, http.HTTPStatus.INTERNAL_SERVER_ERROR
        )


@pytest.mark.unit
def test_handle_exception_for_generic_exception(mock_env):
    """Handle exception correctly logs and returns response for generic
    Exception."""
    # Setup: Create an exception
    exception = Exception("Generic error")

    # Mock the logger
    with patch.object(logger, "error") as mock_log:
        # Act: Call the function with the exception
        response = handle_exception(exception)

        # Assert: Check that the logger was called with the correct arguments
        mock_log.assert_called_with(
            {"message": str(exception), "trace": traceback.format_exc()}
        )

        # Assert: Check that the function returned the correct response
        assert response == generate_response(
            {"message": "An error occurred processing your request."},
            http.HTTPStatus.INTERNAL_SERVER_ERROR,
        )
