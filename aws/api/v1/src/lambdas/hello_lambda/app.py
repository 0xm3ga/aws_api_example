import http
import json
import logging
import os
import traceback
from typing import Dict

# Set up specific logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class InvalidNameError(Exception):
    """Custom error for invalid name input."""

    pass


def validate_input(event: Dict) -> str:
    """
    Validate the input from the event.
    :param event: Lambda event data
    :return: Validated name string
    """
    try:
        name = event.get("queryStringParameters", {}).get("name")
        if not name:
            raise InvalidNameError("Invalid name provided")
        return name
    except InvalidNameError as e:
        logger.error(f"Invalid input: {e}")
        raise


def greet_user(name: str) -> Dict:
    """
    Generate the greeting message.
    :param name: Validated name string
    :return: Response dictionary
    """
    return {"message": f"Hello, {name}!"}


def generate_response(
    body: Dict, status_code: int = http.HTTPStatus.OK
) -> Dict:
    """
    Generate an HTTP response.
    :param body: Response body content
    :param status_code: HTTP status code (default: 200)
    :return: HTTP response dictionary
    """
    DOCS_DOMAIN_NAME = os.getenv("DOCS_DOMAIN_NAME")
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": f"https://{DOCS_DOMAIN_NAME}",
            "Access-Control-Allow-Methods": "OPTIONS,GET,POST,PUT,DELETE",
        },
        "body": json.dumps(body),
    }


def handle_exception(
    e: Exception,
    default_message: str = "An error occurred processing your request.",
) -> Dict:
    """
    Handle exceptions in a uniform way.
    :param e: Exception instance
    :param default_message: Default error message if exception is not specific
        (default: generic server error message)
    :return: HTTP response dictionary
    """
    logger.error({"message": str(e), "trace": traceback.format_exc()})
    error_message = (
        str(e) if isinstance(e, InvalidNameError) else default_message
    )
    return generate_response(
        {"message": error_message}, http.HTTPStatus.INTERNAL_SERVER_ERROR
    )


def lambda_handler(event, context) -> Dict:
    """
    Main Lambda function handler.
    :param event: Lambda event data
    :param context: Lambda context data
    :return: Response dictionary
    """
    try:
        # Log start of function execution and event data
        logger.info(f"Start processing lambda with event: {event}")

        # Process request
        name = validate_input(event)
        response_body = greet_user(name)
        response = generate_response(response_body)

        # Log end of function execution
        logger.info(f"End processing lambda with event: {event}")
    except Exception as e:
        response = handle_exception(e)
    return response
