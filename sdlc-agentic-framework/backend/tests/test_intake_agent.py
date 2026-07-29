import pytest
from app.agents.intake_agent import IntakeAgent
def test_requirement_normalization():
 r=IntakeAgent().run(' Employees submit leave. Managers approve. System maintains audit. '); assert r['id']=='REQ-001'; assert r['feature_name']=='Employee Leave Management System'; assert 'Employee' in r['actors']
def test_missing_input():
 with pytest.raises(ValueError): IntakeAgent().run('short')
