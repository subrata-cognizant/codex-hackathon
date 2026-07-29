import pytest
from pydantic import ValidationError
from app.dto.requirement_dto import WorkflowRequest
from app.agents.implementations import CodeAgent
def test_missing_mandatory_field():
 with pytest.raises(ValidationError): WorkflowRequest()
def test_generated_stub_covers_duplicate(): assert 'duplicate' in CodeAgent().run()['generated_code/leave_feature.py']
def test_approved_and_insufficient_scenarios(sample_data):
 assert any(x['status']=='APPROVED' for x in sample_data['leave_requests']); assert any(x.get('scenario')=='insufficient balance' for x in sample_data['leave_requests'])
