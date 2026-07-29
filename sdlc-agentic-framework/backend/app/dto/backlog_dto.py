from pydantic import BaseModel
class AcceptanceCriterion(BaseModel):
    id: str; given: str; when: str; then: str; requirement_id: str = "REQ-001"
class UserStory(BaseModel):
    id: str; title: str; persona: str; narrative: str; story_points: int; priority: str; dependencies: list[str]; subtasks: list[str]; acceptance_criteria: list[AcceptanceCriterion]
class Epic(BaseModel):
    id: str; title: str; stories: list[UserStory]
class BacklogDTO(BaseModel):
    requirement_id: str; epics: list[Epic]
