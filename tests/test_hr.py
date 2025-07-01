import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
import pytest
from mocks.hr_service import app as hr_app

client = TestClient(hr_app)

def test_create_and_get_employee():
    # Create an employee
    payload = {"name": "Alice", "email": "alice@example.com", "title": "Engineer"}
    resp = client.post("/employees", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "employee_id" in data

    emp_id = data["employee_id"]
    # Retrieve the employee
    resp2 = client.get(f"/employees/{emp_id}")
    assert resp2.status_code == 200
    assert resp2.json()["email"] == "alice@example.com"

def test_get_nonexistent_employee():
    resp = client.get("/employees/not-exist")
    assert resp.status_code == 404