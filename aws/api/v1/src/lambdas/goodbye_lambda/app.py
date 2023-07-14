import http
import json
import logging
import os
import traceback
from typing import Dict

from utils.errors import (
    DEFAULT_HTTP_ERROR,
    INVALID_NAME_ERROR,
    JSON_SERIALIZING_ERROR,
    REQUIRED_NAME_ERROR,
    UNEXPECTED_HTTP_ERROR,
    CustomError,
    InvalidQueryStringParameterError,
    MissingRequiredQueryStringParameterError,
)
from utils.logging import ENDED_PROCESSING_LOG, STARTED_PROCESSING_LOG

# Set up specific logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def validate_input(event: Dict) -> str:
    """
    Validate the input from the event.
    :param event: Lambda event data
    :return: Validated name string
    """
    query_parameters = event.get("queryStringParameters", {})

    if not query_parameters:
        raise MissingRequiredQueryStringParameterError(REQUIRED_NAME_ERROR)

    if "name" not in query_parameters:
        raise MissingRequiredQueryStringParameterError(REQUIRED_NAME_ERROR)

    name = query_parameters.get("name")
    if not name or name.strip() == "":
        raise InvalidQueryStringParameterError(INVALID_NAME_ERROR)

    return name


def greet_user(name: str) -> Dict:
    """
    Generate the greeting message.
    :param name: Validated name string
    :return: Response dictionary
    """
    return {"message": f"Goodbye, {name}!"}


def generate_response(body: Dict, status_code: int = http.HTTPStatus.OK) -> Dict:
    """
    Generate an HTTP response.
    :param body: Response body content
    :param status_code: HTTP status code (default: 200)
    :return: HTTP response dictionary
    """
    DOCS_DOMAIN_NAME = os.getenv("DOCS_DOMAIN_NAME")

    try:
        body_json = json.dumps(body)
    except TypeError as e:
        logger.error(JSON_SERIALIZING_ERROR.format(e))
        body_json = json.dumps({"error": UNEXPECTED_HTTP_ERROR})
        status_code = http.HTTPStatus.INTERNAL_SERVER_ERROR

    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": f"https://{DOCS_DOMAIN_NAME}",
            "Access-Control-Allow-Methods": "OPTIONS,GET,POST,PUT,DELETE",
        },
        "body": body_json,
    }


def handle_exception(
    e: Exception,
    default_message: str = DEFAULT_HTTP_ERROR,
) -> Dict:
    """
    Handle exceptions in a uniform way.
    :param e: Exception instance
    :param default_message: Default error message if exception is not specific
        (default: generic server error message)
    :return: HTTP response dictionary
    """
    logger.error({"error": str(e), "trace": traceback.format_exc()})

    status_code = (
        e.status_code if isinstance(e, CustomError) else http.HTTPStatus.INTERNAL_SERVER_ERROR
    )
    error_message = str(e) if isinstance(e, CustomError) else default_message

    return generate_response({"error": error_message}, status_code)


def lambda_handler(event, context) -> Dict:
    """
    Main Lambda function handler.
    :param event: Lambda event data
    :param context: Lambda context data
    :return: Response dictionary
    """
    try:
        # Log start of function execution and event data
        logger.info(STARTED_PROCESSING_LOG.format(event))

        # Process request
        name = validate_input(event)
        response_body = greet_user(name)
        response = generate_response(response_body)

        # Log end of function execution
        logger.info(ENDED_PROCESSING_LOG.format(event))
    except Exception as e:
        response = handle_exception(e)
    return response
