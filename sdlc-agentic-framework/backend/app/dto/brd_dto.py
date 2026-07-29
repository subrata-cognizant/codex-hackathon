from pydantic import BaseModel
class BRDArtifact(BaseModel):
    id: str = "BRD-001"; requirement_id: str = "REQ-001"; content: str; confidence: dict[str, float]
