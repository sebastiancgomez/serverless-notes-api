import json
from service.app.router import handle_request
import pytest

@pytest.fixture
def lambda_event():
    def _build_event(path, method="POST", body=None):
        return {
            "httpMethod": method,
            "path": f"/default{path}",
            "headers": {},
            "body": json.dumps(body) if body else None
        }
    return _build_event


@pytest.fixture
def login_body():
    def _build(username, password):
        return {
            "username": username,
            "password": password
        }
    return _build


def test_login_success(lambda_event, login_body):
    # Arrange
    body = login_body("sebastian", "123456")

    event = lambda_event(
        path="/auth/login",
        method="POST",
        body=body
    )

    # Act
    response = handle_request(None, event)

    # Assert
    assert response["statusCode"] == 200

    data = json.loads(response["body"])

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_password(lambda_event, login_body):
    # Arrange
    body = login_body("sebastian", "wrongpass")

    event = lambda_event(
        path="/auth/login",
        method="POST",
        body=body
    )

    # Act
    response = handle_request(None, event)

    # Assert
    assert response["statusCode"] == 401

    data = json.loads(response["body"])

    assert data["error"] == "Invalid credentials"


def test_login_missing_body(lambda_event):
    # Arrange
    event = lambda_event(
        path="/auth/login",
        method="POST",
        body=None
    )

    # Act
    response = handle_request(None, event)

    # Assert
    assert response["statusCode"] == 400

    data = json.loads(response["body"])

    assert data["error"] == "Missing body"