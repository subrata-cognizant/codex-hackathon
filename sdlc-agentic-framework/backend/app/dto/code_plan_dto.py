from pydantic import BaseModel
class CodePlanDTO(BaseModel):
    requirement_id: str; story_ids: list[str]; content: str; approved: bool = False
