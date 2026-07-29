from fastapi import APIRouter, HTTPException, Request, status
from app.dto.leave_dto import LeaveDecision, LeaveRequestCreate
from app.services.leave_service import LeaveDomainError
router=APIRouter(prefix="/api/leave",tags=["demo feature"])
def execute(action):
    try: return action()
    except LeaveDomainError as error: raise HTTPException(status.HTTP_409_CONFLICT,{"code":error.code,"message":str(error)}) from error
@router.post("/requests",status_code=status.HTTP_201_CREATED)
def submit(body:LeaveRequestCreate,request:Request): return execute(lambda:request.app.state.leave.submit(body))
@router.post("/requests/{request_id}/decision")
def decide(request_id:str,body:LeaveDecision,request:Request): return execute(lambda:request.app.state.leave.decide(request_id,body))
@router.get("/balances/{employee_id}")
def balance(employee_id:str,request:Request): return execute(lambda:request.app.state.leave.balance(employee_id))
