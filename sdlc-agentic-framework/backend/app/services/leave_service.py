from datetime import datetime
from uuid import uuid4
from app.dto.leave_dto import LeaveDecision, LeaveRequestCreate
from app.repositories.sqlite_leave_repository import SQLiteLeaveRepository

class LeaveDomainError(ValueError):
    def __init__(self, code: str, message: str): self.code=code; super().__init__(message)

class LeaveService:
    def __init__(self, repository: SQLiteLeaveRepository): self.repository=repository

    def balance(self, employee_id: str) -> dict:
        employee=self.repository.employee(employee_id)
        if not employee: raise LeaveDomainError("EMPLOYEE_NOT_FOUND", "Employee was not found")
        return {"employee_id":employee_id,"available_days":employee["balance"],"traceability":["REQ-001","STORY-003","AC-003"]}

    def submit(self, request: LeaveRequestCreate) -> dict:
        employee=self.repository.employee(request.employee_id)
        if not employee: raise LeaveDomainError("EMPLOYEE_NOT_FOUND", "Employee was not found")
        # Dates are authoritative: never trust a caller-supplied duration for
        # entitlement checks or persistence.
        requested_days=(request.end_date-request.start_date).days+1
        if requested_days > employee["balance"]: raise LeaveDomainError("INSUFFICIENT_BALANCE", "Requested days exceed available leave balance")
        if self.repository.overlapping(request.employee_id,request.start_date.isoformat(),request.end_date.isoformat()): raise LeaveDomainError("DUPLICATE_REQUEST", "An overlapping pending or approved leave request exists")
        record={**request.model_dump(mode="json"),"days":requested_days,"id":f"LR-{uuid4().hex[:8].upper()}","manager_id":employee["manager_id"],"status":"PENDING","created_at":datetime.utcnow().isoformat()}
        return {**self.repository.create(record),"traceability":["REQ-001","STORY-001","AC-001","CODE-001"]}

    def decide(self, request_id: str, decision: LeaveDecision) -> dict:
        current=self.repository.get(request_id)
        if not current: raise LeaveDomainError("REQUEST_NOT_FOUND", "Leave request was not found")
        if current["manager_id"] != decision.manager_id: raise LeaveDomainError("FORBIDDEN_MANAGER", "Only the assigned manager can decide this request")
        if current["status"] != "PENDING": raise LeaveDomainError("INVALID_STATUS", "Only pending requests can be decided")
        try:
            decided=self.repository.decide(request_id,decision.decision,decision.manager_id)
        except ValueError as error:
            if "balance" in str(error).lower():
                raise LeaveDomainError("INSUFFICIENT_BALANCE", "Available leave balance changed before approval") from error
            raise LeaveDomainError("INVALID_STATUS", "Only pending requests can be decided") from error
        return {**decided,"traceability":["REQ-001","STORY-002","AC-002","CODE-002"]}
