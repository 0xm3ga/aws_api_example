# import http

# import requests

# API_ENDPOINT = "http://localhost:3000"


# def test_hello_lambda():
#     response = requests.get(f"{API_ENDPOINT}/hello?name=John")
#     assert response.status_code == 200

#     data = response.json()
#     assert data["message"] == "Hello, John!"


# def test_hello_lambda_no_name():
#     response = requests.get(f"{API_ENDPOINT}/hello")
#     print(response)
#     assert response.status_code == http.HTTPStatus.BAD_REQUEST

#     data = response.json()
#     assert "Name query string parameter is required" in data["message"]


# def test_goodbye_lambda():
#     response = requests.get(f"{API_ENDPOINT}/goodbye?name=John")
#     assert response.status_code == 200

#     data = response.json()
#     assert data["message"] == "Goodbye, John!"


# def test_goodbye_lambda_no_name():
#     response = requests.get(f"{API_ENDPOINT}/goodbye")
#     assert response.status_code == http.HTTPStatus.BAD_REQUEST

#     data = response.json()
#     assert "Invalid name provided" in data["message"]
