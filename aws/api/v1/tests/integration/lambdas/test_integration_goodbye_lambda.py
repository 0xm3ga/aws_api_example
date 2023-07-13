import http

import pytest
import requests

from utils.errors import INVALID_NAME_ERROR, REQUIRED_NAME_ERROR

API_ENDPOINT = "http://localhost:3000/"


def make_request(endpoint, params=None):
    try:
        response = requests.get(f"{API_ENDPOINT}/{endpoint}", params=params)
    except Exception as e:
        pytest.fail(f"Request to {endpoint} endpoint failed: {e}")
    return response


@pytest.mark.integration
def test_hello_lambda():
    response = make_request("goodbye", params={"name": "John"})
    assert response.status_code == http.HTTPStatus.OK
    data = response.json()
    assert data["message"] == "Goodbye, John!"


@pytest.mark.integration
@pytest.mark.parametrize(
    "params,expected_status_code,expected_error_message",
    [
        ({}, http.HTTPStatus.BAD_REQUEST, REQUIRED_NAME_ERROR),
        ({"name1": "World"}, http.HTTPStatus.BAD_REQUEST, REQUIRED_NAME_ERROR),
        ({"name": ""}, http.HTTPStatus.BAD_REQUEST, INVALID_NAME_ERROR),
        ({"name": " "}, http.HTTPStatus.BAD_REQUEST, INVALID_NAME_ERROR),
    ],
)
def test_hello_lambda_errors(params, expected_status_code, expected_error_message):
    response = make_request("goodbye", params=params)
    assert response.status_code == expected_status_code
    data = response.json()
    assert data["error"] == expected_error_message
