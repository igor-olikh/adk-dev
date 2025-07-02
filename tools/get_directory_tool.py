import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="get_directory_tool", description="Get directory information for an employee", permission=ToolPermission.READ_ONLY)
def get_directory_info(email: str) -> str:
    """
    Get directory information for an employee by email address.
    
    Args:
        email: The email address of the employee to look up
    
    Returns:
        str: Directory information or error message
    """
    
    if not email:
        return "Missing required parameter: email"
    
    # Call the mock Directory service running on port 8002
    url = f"http://localhost:8002/directory/{email}"
    headers = {"Authorization": "Bearer TBD"}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            return f"✅ Found directory entry for {email}: Department: {data.get('department', 'N/A')}, Manager: {data.get('manager', 'N/A')}"
        elif response.status_code == 404:
            return f"❌ No directory entry found for email: {email}"
        else:
            return f"❌ Directory lookup failed. Status: {response.status_code}, Response: {response.text}"
            
    except requests.exceptions.ConnectionError:
        return "❌ Error: Could not connect to Directory service. Please ensure the mock Directory service is running on port 8002."
    except requests.exceptions.Timeout:
        return "❌ Error: Request to Directory service timed out."
    except requests.exceptions.RequestException as e:
        return f"❌ Error looking up directory info: {str(e)}"