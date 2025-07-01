from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class DirectoryEntry(BaseModel):
    email: str
    department: str
    manager: str

dir_db = {
    "alice@example.com": {"email": "alice@example.com", "department": "HR", "manager": "bob@example.com"}
}

@app.get("/directory/{email}", response_model=DirectoryEntry)
def get_directory(email: str):
    entry = dir_db.get(email)
    if not entry:
        raise HTTPException(status_code=404, detail="Not found")
    return entry