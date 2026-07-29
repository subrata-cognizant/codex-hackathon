from fastapi import APIRouter,HTTPException,Request
router=APIRouter(prefix='/api',tags=['artifacts'])
@router.get('/health')
def health(): return {'status':'ok','mode':'local-first'}
@router.get('/artifacts')
def artifacts(request:Request): return request.app.state.artifacts.list()
@router.get('/artifacts/{artifact_name:path}')
def artifact(artifact_name:str,request:Request):
    try:return request.app.state.artifacts.get(artifact_name)
    except FileNotFoundError as e: raise HTTPException(404,'Artifact not found') from e
@router.get('/traceability')
def traceability(request:Request):
    try:return request.app.state.traceability.get()
    except FileNotFoundError as e: raise HTTPException(404,'Run and approve a workflow first') from e
