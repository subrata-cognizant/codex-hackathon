"""Pydantic contracts for the runnable leave-management demo feature."""
from datetime import date, datetime
from typing import Literal
from pydantic import BaseModel, Field, model_validator

LeaveStatus = Literal["PENDING", "APPROVED", "REJECTED", "CANCELLED"]

class LeaveRequestCreate(BaseModel):
    employee_id: str = Field(min_length=1)
    start_date: date
    end_date: date
    days: int = Field(gt=0, le=30)
    reason: str = Field(min_length=3, max_length=250)

    @model_validator(mode="after")
    def validate_dates(self) -> "LeaveRequestCreate":
        if self.end_date < self.start_date:
            raise ValueError("end_date must be on or after start_date")
        return self

class LeaveDecision(BaseModel):
    manager_id: str = Field(min_length=1)
    decision: Literal["APPROVED", "REJECTED"]
    comment: str = Field(default="", max_length=250)

class LeaveRequestDTO(LeaveRequestCreate):
    id: str
    status: LeaveStatus
    manager_id: str
    created_at: datetime
    traceability: list[str] = ["REQ-001", "STORY-001", "AC-001"]

class LeaveBalanceDTO(BaseModel):
    employee_id: str
    available_days: int
