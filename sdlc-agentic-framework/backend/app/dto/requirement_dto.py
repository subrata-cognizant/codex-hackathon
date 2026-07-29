from pydantic import BaseModel, Field

class WorkflowRequest(BaseModel):
    requirement_text: str = Field(min_length=10)

class RequirementDTO(BaseModel):
    id: str = "REQ-001"
    feature_name: str
    raw_text: str
    actors: list[str]
    business_rules: list[dict]
    assumptions: list[dict]
    constraints: list[str]
    non_functional_requirements: list[dict]
    open_questions: list[dict]
    traceability_references: list[str] = []
