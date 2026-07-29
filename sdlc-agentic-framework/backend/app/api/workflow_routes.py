from fastapi import APIRouter, HTTPException, Request
from app.dto.requirement_dto import WorkflowRequest
router=APIRouter(prefix='/api/workflow',tags=['workflow'])
def call(fn):
    try: return fn()
    except ValueError as e: raise HTTPException(409,str(e)) from e
@router.post('/run')
def run(body:WorkflowRequest,request:Request): return call(lambda:request.app.state.workflow.run(body.requirement_text))
@router.post('/approve/brd')
def approve_brd(request:Request): return call(request.app.state.workflow.approve_brd)
@router.post('/approve/code-plan')
def approve_code(request:Request): return call(request.app.state.workflow.approve_code_plan)

@router.get('/status')
def status(request:Request): return request.app.state.workflow.status()

@router.get('/audit')
def audit(request:Request): return {'events':request.app.state.workflow.audit}
