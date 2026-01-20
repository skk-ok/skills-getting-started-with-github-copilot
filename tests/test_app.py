import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200 or response.status_code == 307
    assert "text/html" in response.headers.get("content-type", "")

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_for_activity_success():
    response = client.post("/activities/Chess Club/signup?email=tester@mergington.edu")
    assert response.status_code == 200
    assert "Signed up" in response.json().get("message", "")

def test_signup_for_activity_duplicate():
    # First signup
    client.post("/activities/Programming Class/signup?email=dupe@mergington.edu")
    # Duplicate signup
    response = client.post("/activities/Programming Class/signup?email=dupe@mergington.edu")
    assert response.status_code == 400
    assert "already signed up" in response.json().get("detail", "")

def test_signup_for_nonexistent_activity():
    response = client.post("/activities/Nonexistent/signup?email=ghost@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json().get("detail", "")
