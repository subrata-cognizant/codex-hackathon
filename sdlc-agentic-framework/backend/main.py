from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.api.leave_routes import router as leave_router
from app.api.workflow_routes import router as workflow_router
from app.core.config import ARTIFACT_DIR, DATA_DIR
from app.repositories.json_repository import JsonRepository
from app.repositories.sqlite_leave_repository import SQLiteLeaveRepository
from app.services.artifact_service import ArtifactService
from app.services.leave_service import LeaveService
from app.services.traceability_service import TraceabilityService
from app.services.workflow_service import WorkflowService

app=FastAPI(title="SDLC Agentic Framework",version="1.1.0")
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:3000","http://localhost:5173"],allow_methods=["*"],allow_headers=["*"])
artifact_repo=JsonRepository(ARTIFACT_DIR)
app.state.workflow=WorkflowService(artifact_repo,DATA_DIR/"mock_knowledge_graph.json")
app.state.artifacts=ArtifactService(artifact_repo)
app.state.traceability=TraceabilityService(artifact_repo)
app.state.leave=LeaveService(SQLiteLeaveRepository(DATA_DIR/"leave_demo.db"))
app.include_router(workflow_router); app.include_router(leave_router); app.include_router(router)
