from fastapi.testclient import TestClient
from mocks.directory_service import app as dir_app

client = TestClient(dir_app)

def test_get_existing_directory_entry():
    resp = client.get("/directory/alice@example.com")
    assert resp.status_code == 200
    data = resp.json()
    assert data["department"] == "HR"
    assert data["manager"] == "bob@example.com"

def test_get_nonexistent_directory_entry():
    resp = client.get("/directory/unknown@example.com")
    assert resp.status_code == 404