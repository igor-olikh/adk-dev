import uuid
from datetime import datetime
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
    
    # Mock meeting scheduling - generate a unique meeting ID
    meeting_id = str(uuid.uuid4())
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Validate participants list
    if not isinstance(participants, list) or len(participants) == 0:
        return "Error: participants must be a non-empty list of email addresses"
    
    # Mock successful meeting creation
    participant_list = ", ".join(participants)
    
    return f"✅ Successfully scheduled meeting '{subject}' with ID {meeting_id[:8]}... for {start_time} (duration: {duration_minutes} minutes). Participants: {participant_list}. Created at: {current_time}" 