import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="create_profile", description="Create a new profile", permission=ToolPermission.READ_WRITE)
def create_profile(name: str, email: str, title: str) -> str:

    name = name or "Unknown"
    email = email or "unknown@example.com"
    title = title or "Employee"

    payload = {
        "name": name,
        "email": email,
        "title": title
    }

    # Call the mock HR system running on port 8001
    url = "http://localhost:8001/employees"
    headers = {"Authorization": f"Bearer {"TBD"}"}

    response = requests.post(url, json=payload, headers=headers, timeout=5)

    if response.status_code != 200:
        return f"Failed to create profile. Status code: {response.status_code}, Response: {response.text}"

    return f"Created new employee profile with email {email}"