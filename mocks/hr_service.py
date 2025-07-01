from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uuid
from datetime import datetime

app = FastAPI()

class Employee(BaseModel):
    name: str
    email: str
    title: str

class Meeting(BaseModel):
    subject: str
    participants: List[str]
    start_time: str
    duration_minutes: int = 60

db = {}
meetings_db = {}

@app.post("/employees", response_model=dict)
def create_employee(emp: Employee):
    emp_id = str(uuid.uuid4())
    db[emp_id] = emp.model_dump()
    return {"employee_id": emp_id}

@app.get("/employees/{emp_id}", response_model=Employee)
def get_employee(emp_id: str):
    if emp_id not in db:
        raise HTTPException(status_code=404, detail="Not found")
    return db[emp_id]

@app.patch("/employees/{emp_id}", response_model=Employee)
def update_employee(emp_id: str, emp_updates: Employee):
    if emp_id not in db:
        raise HTTPException(status_code=404, detail="Not found")
    db[emp_id].update(emp_updates.dict(exclude_unset=True))
    return db[emp_id]

@app.post("/meetings", response_model=dict)
def create_meeting(meeting: Meeting):
    meeting_id = str(uuid.uuid4())
    meeting_data = meeting.dict()
    meeting_data["meeting_id"] = meeting_id
    meeting_data["created_at"] = datetime.now().isoformat()
    meetings_db[meeting_id] = meeting_data
    return {"meeting_id": meeting_id, "status": "scheduled"}

@app.get("/meetings/{meeting_id}", response_model=Meeting)
def get_meeting(meeting_id: str):
    if meeting_id not in meetings_db:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meetings_db[meeting_id]

@app.get("/meetings", response_model=List[dict])
def list_meetings():
    return list(meetings_db.values())