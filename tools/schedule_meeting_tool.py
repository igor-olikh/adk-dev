import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="schedule_meeting_tool", description="Schedule a meeting with specified participants", permission=ToolPermission.READ_WRITE)
def schedule_meeting(subject: str, participants: list, start_time: str, duration_minutes: int = 60) -> str:
    """
    Schedule a meeting with the specified participants.
    
    Args:
        subject: The meeting subject/title
        participants: List of participant email addresses
        start_time: Start time in ISO format (YYYY-MM-DDTHH:MM:SS)
        duration_minutes: Meeting duration in minutes (default: 60)
    
    Returns:
        str: Success or error message
    """
    
    if not subject or not participants or not start_time:
        return "Missing required parameters: subject, participants, and start_time are required"
    
    payload = {
        "subject": subject,
        "participants": participants,
        "start_time": start_time,
        "duration_minutes": duration_minutes
    }
    
    # Call the mock HR system running on port 8001
    url = "http://localhost:8001/meetings"
    headers = {"Authorization": f"Bearer {"TBD"}"}
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        
        if response.status_code == 201:
            meeting_data = response.json()
            return f"Successfully scheduled meeting '{subject}' with ID {meeting_data.get('meeting_id')} for {start_time}"
        else:
            return f"Failed to schedule meeting. Status code: {response.status_code}, Response: {response.text}"
            
    except requests.exceptions.RequestException as e:
        return f"Error scheduling meeting: {str(e)}" 