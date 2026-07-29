import json,pytest
from app.services.workflow_service import WorkflowService
from app.repositories.json_repository import JsonRepository
def make(tmp_path):
 k=tmp_path/'k.json'; k.write_text(json.dumps({'related_brds':[],'reusable_patterns':[],'previous_decisions':[],'code_modules':[],'risks':[]})); return WorkflowService(JsonRepository(tmp_path/'out'),k)
def test_complete_workflow(tmp_path):
 s=make(tmp_path); assert s.run('Employees submit leave and managers approve with audit trail.')['status']=='awaiting_brd_approval'; assert s.approve_brd()['status']=='awaiting_code_plan_approval'; result=s.approve_code_plan(); assert result['status']=='complete'; assert 'lineage_graph.json' in result['artifact_references']
def test_duplicate_requirement(tmp_path):
 s=make(tmp_path); text='Employees submit leave and managers approve with audit trail.'; s.run(text)
 with pytest.raises(ValueError,match='Duplicate'): s.run(text)
def test_invalid_gate(tmp_path):
 with pytest.raises(ValueError): make(tmp_path).approve_brd()
def test_non_leave_requirement_drives_brd_and_backlog(tmp_path):
 s=make(tmp_path); result=s.run('Users submit invoices and finance managers approve payments with an audit trail.')
 assert 'Employee Leave' not in result['brd']
 assert 'Users submit invoices' in result['brd']
 backlog=s.approve_brd()['backlog']
 assert 'invoice' in backlog['epics'][0]['title'].lower()
 assert all('leave' not in story['title'].lower() for story in backlog['epics'][0]['stories'])
