# CODE-001 implements STORY-001 / AC-001
from pydantic import BaseModel
class LeaveRequestCreate(BaseModel):
    employee_id: str
    start_date: str
    end_date: str
class LeaveRepository:
    def __init__(self): self.requests=[]
class LeaveService:
    def __init__(self, repository): self.repository=repository
    def submit(self, request):
        if request in self.repository.requests: raise ValueError("duplicate leave request")
        self.repository.requests.append(request); return {"status":"pending"}
