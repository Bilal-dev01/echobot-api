import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "Echobot API is running" in data["message"]

def test_chat_endpoint(client):
    """Test the chat endpoint with valid input."""
    test_message = "Hello, world!"
    response = client.post("/chat", json={"message": test_message})
    assert response.status_code == 200
    data = response.json()
    assert data["reply"] == f"You said: {test_message}"

def test_chat_endpoint_empty_message(client):
    """Test the chat endpoint with empty message."""
    response = client.post("/chat", json={"message": ""})
    assert response.status_code == 422  # Validation error

def test_chat_endpoint_long_message(client):
    """Test the chat endpoint with message exceeding max length."""
    long_message = "a" * 1001  # Exceeds max_length=1000
    response = client.post("/chat", json={"message": long_message})
    assert response.status_code == 422  # Validation error 