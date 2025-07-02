import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="create_profile_tool", description="Create a new profile", permission=ToolPermission.READ_WRITE)
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
    headers = {"Authorization": "Bearer TBD"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            return f"✅ Successfully created new employee profile for {name} ({email}) with title '{title}'. Employee ID: {data.get('employee_id', 'N/A')}"
        else:
            return f"❌ Failed to create profile. Status code: {response.status_code}, Response: {response.text}"
            
    except requests.exceptions.ConnectionError:
        return "❌ Error: Could not connect to HR service. Please ensure the mock HR service is running on port 8001."
    except requests.exceptions.Timeout:
        return "❌ Error: Request to HR service timed out."
    except requests.exceptions.RequestException as e:
        return f"❌ Error creating profile: {str(e)}"