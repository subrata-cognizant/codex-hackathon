from datetime import date
import pytest
from pydantic import ValidationError
from app.dto.leave_dto import LeaveDecision, LeaveRequestCreate
from app.repositories.sqlite_leave_repository import SQLiteLeaveRepository
from app.services.leave_service import LeaveDomainError, LeaveService
@pytest.fixture
def service(tmp_path): return LeaveService(SQLiteLeaveRepository(tmp_path/"test.db"))
def request(employee="E001",start=date(2027,1,10),days=2): return LeaveRequestCreate(employee_id=employee,start_date=start,end_date=date(2027,1,11),days=days,reason="Family event")
def test_approved_request(service):
 created=service.submit(request()); decided=service.decide(created["id"],LeaveDecision(manager_id="M001",decision="APPROVED")); assert decided["status"]=="APPROVED"; assert "AC-002" in decided["traceability"]
def test_duplicate_request(service):
 service.submit(request())
 with pytest.raises(LeaveDomainError) as error: service.submit(request())
 assert error.value.code=="DUPLICATE_REQUEST"
def test_eligibility_failure(service):
 with pytest.raises(LeaveDomainError) as error: service.submit(request(employee="E002",days=3))
 assert error.value.code=="INSUFFICIENT_BALANCE"
def test_missing_mandatory_and_invalid_date():
 with pytest.raises(ValidationError): LeaveRequestCreate(start_date="2027-01-10",end_date="2027-01-11",days=1,reason="Trip")
 with pytest.raises(ValidationError): LeaveRequestCreate(employee_id="E001",start_date="2027-01-12",end_date="2027-01-11",days=1,reason="Trip")
def test_edge_cases(service):
 assert service.balance("E004")["available_days"]==0
 created=service.submit(request())
 with pytest.raises(LeaveDomainError) as error: service.decide(created["id"],LeaveDecision(manager_id="M002",decision="APPROVED"))
 assert error.value.code=="FORBIDDEN_MANAGER"
