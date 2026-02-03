from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister():
    activity = "Chess Club"
    email = "test_student@example.com"

    # Ensure clean state: remove if already present
    res = client.get("/activities")
    participants = res.json()[activity]["participants"]
    if email in participants:
        client.delete(f"/activities/{activity}/participants?email={email}")

    # Sign up
    res = client.post(f"/activities/{activity}/signup?email={email}")
    assert res.status_code == 200
    assert "Signed up" in res.json().get("message", "")

    # Confirm added
    res = client.get("/activities")
    assert email in res.json()[activity]["participants"]

    # Unregister
    res = client.delete(f"/activities/{activity}/participants?email={email}")
    assert res.status_code == 200
    assert "Unregistered" in res.json().get("message", "")

    # Confirm removed
    res = client.get("/activities")
    assert email not in res.json()[activity]["participants"]


def test_duplicate_signup_returns_400():
    activity = "Basketball"
    # Use an email that initially exists for Basketball
    existing_email = "alex@mergington.edu"
    res = client.post(f"/activities/{activity}/signup?email={existing_email}")
    assert res.status_code == 400


def test_unregister_nonexistent_returns_404():
    res = client.delete("/activities/Programming%20Class/participants?email=not-there@example.com")
    assert res.status_code == 404
