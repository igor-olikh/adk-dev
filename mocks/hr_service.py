from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid

app = FastAPI()

class Employee(BaseModel):
    name: str
    email: str
    title: str

db = {}

@app.post("/employees", response_model=dict)
def create_employee(emp: Employee):
    emp_id = str(uuid.uuid4())
    db[emp_id] = emp.dict()
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