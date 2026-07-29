import re
from pathlib import Path
from app.dto.requirement_dto import RequirementDTO

class IntakeAgent:
    def run(self, text: str) -> dict:
        clean=' '.join(text.split())
        if len(clean)<10: raise ValueError('Requirement must contain at least 10 characters')
        low=clean.lower(); actors=[a for a in ['Employee','Manager','System'] if a.lower() in low]
        rules=[]
        candidates=[('insufficient','Employee cannot apply leave if leave balance is insufficient'),('duplicate','Duplicate leave requests must be prevented'),('mandatory','Manager approval is mandatory'),('audit','Audit trail captures every action')]
        for key,value in candidates:
            if key in low: rules.append({'id':f'RULE-{len(rules)+1:03d}','text':value})
        if not rules: rules=[{'id':'RULE-001','text':'All workflow actions must be validated'}]
        nfr=[]
        for key,value in [('fast','Fast response for normal operations'),('error','Clear error messages'),('integration','Support future HR integration'),('mandatory fields','Validate mandatory fields')]:
            if key in low: nfr.append({'id':f'NFR-{len(nfr)+1:03d}','text':value})
        if not nfr: nfr=[{'id':'NFR-001','text':'Secure, responsive local operation'}]
        feature='Employee Leave Management System' if 'leave' in low else clean.split('.')[0][:80]
        return RequirementDTO(feature_name=feature,raw_text=clean,actors=actors or ['User'],business_rules=rules,assumptions=[{'id':'ASSUMPTION-001','text':'Identity and role data is available'}],constraints=['Local-first JSON persistence'],non_functional_requirements=nfr,open_questions=[{'id':'QUESTION-001','text':'What notification channels are required?'}],traceability_references=['BRD-001']).model_dump()

class ContextAgent:
    def run(self, req, knowledge):
        return {'requirement_id':req['id'],'related_brds':knowledge['related_brds'],'reusable_patterns':knowledge['reusable_patterns'],'previous_decisions':knowledge['previous_decisions'],'related_code_modules':knowledge['code_modules'],'known_risk_areas':knowledge['risks']}
class ClarificationAgent:
    def run(self, req): return '# Clarifications — REQ-001\n\n- Which notification channels are required?\n- What is the leave calendar policy?\n\n**Assumption:** email notification is sufficient for the PoC.\n\n**Confidence:** 0.78\n'
class BRDAgent:
    def run(self, req, context):
        sections={'Executive Summary':f"Automate {req['feature_name']} with traceable approvals.",'Business Objective':'Reduce manual handoffs and ensure reliable leave decisions.','Scope':'Submit, balance check, approve/reject, notify, and audit.','Out of Scope':'Payroll and production identity integration.','Functional Requirements':'FR-001 submit request; FR-002 check balance; FR-003 manager decision; FR-004 audit and notify.','Non-Functional Requirements':'; '.join(x['text'] for x in req['non_functional_requirements']),'Assumptions':req['assumptions'][0]['text'],'Constraints':'; '.join(req['constraints']),'Risks':'Concurrent requests and notification delivery.','Dependencies':'Employee directory and leave policy.','Acceptance Criteria Summary':'Valid requests become pending; invalid or duplicate requests are rejected.'}
        return '# BRD-001 — Employee Leave Management\n\n**Traceability:** REQ-001\n\n'+''.join(f'## {k} (confidence: 0.90)\n{v}\n\n' for k,v in sections.items())
class StoryAgent:
    def run(self, brd):
        specs=[('STORY-001','Submit leave request','Employee','submit a valid request','it is validated','a pending request and audit record are created'),('STORY-002','Decide leave request','Manager','approve or reject a pending request','a decision is recorded','balance, notification, and audit are updated'),('STORY-003','Check leave balance','Employee','view my balance','the balance is requested','the current available balance is shown')]
        stories=[]
        for i,(sid,title,persona,when,given,then) in enumerate(specs,1): stories.append({'id':sid,'title':title,'persona':persona,'narrative':f'As an {persona}, I want to {title.lower()} so that leave is managed.','story_points':[5,3,2][i-1],'priority':'High','dependencies':[] if i==1 else ['STORY-001'],'subtasks':['API and validation','UI and tests'],'acceptance_criteria':[{'id':f'AC-{i:03d}','given':given,'when':when,'then':then,'requirement_id':'REQ-001'}]})
        return {'requirement_id':'REQ-001','epics':[{'id':'EPIC-001','title':'Leave lifecycle','stories':stories}]}
class SprintPlanAgent:
    def run(self,b): return '# Sprint Plan\n**Traceability:** REQ-001, EPIC-001, STORY-001..003\n\n## Allocation\nSprint 1: STORY-001 and STORY-003. Sprint 2: STORY-002.\n## Sequence and critical path\nData model → submission → approval → notifications.\n## Risk flags\nConcurrent duplicate submissions.\n## Definition of Ready\nAcceptance criteria and dependencies reviewed.\n## Definition of Done\nTests pass, review complete, lineage recorded.\n'
class CodePlanAgent:
    def run(self,b): return '# Code Plan\n**Traceability:** REQ-001; STORY-001..003; AC-001..003\n\n## Architecture\nFastAPI router → service → JSON repository; React form → REST API.\n## APIs\nPOST /leave-requests; GET /leave-balances/{employee_id}.\n## DTOs and data model\nLeaveRequestCreate, LeaveRequest; employee, date range, status.\n## Services / Controllers\nLeaveService and leave router.\n## Frontend\nLeave request form and status panel.\n## Unit test plan\nApproved, duplicate, insufficient balance, missing fields.\n## AC mapping\nAC-001 → submit endpoint/test; AC-002 → decision service/test; AC-003 → balance endpoint/test.\n'
class CodeAgent:
    def run(self): return {'generated_code/leave_feature.py':'''from pydantic import BaseModel\nclass LeaveRequestCreate(BaseModel):\n    employee_id: str\n    start_date: str\n    end_date: str\nclass LeaveRepository:\n    def __init__(self): self.requests=[]\nclass LeaveService:\n    def __init__(self, repo): self.repo=repo\n    def submit(self, item):\n        if any(x.employee_id==item.employee_id and x.start_date==item.start_date and x.end_date==item.end_date for x in self.repo.requests): raise ValueError("duplicate leave request")\n        self.repo.requests.append(item); return {"status":"pending","traceability":"AC-001"}\n# Router: POST /leave-requests delegates to LeaveService.submit\n''','generated_code/LeaveRequestPage.tsx':'''export const LeaveRequestPage=()=> <form><h2>Submit leave request</h2><input aria-label="Employee ID"/><button>Submit</button></form>; // STORY-001 / AC-001\n''','generated_code/test_leave_feature.py':'''def test_submit_template():\n    # TEST-001 traces AC-001\n    assert True\n'''}
class ReviewAgent:
    def run(self): return '# Review Report\n**REVIEW-001 | Traceability:** BRD-001, STORY-001, AC-001, CODE-001\n\n- PASS: Layer boundaries and mandatory DTO fields.\n- PASS: Duplicate validation and clear exception.\n- FINDING-001 (Medium): add authentication before production.\n- FINDING-002 (Low): use date types rather than strings.\n'
class SanityAgent:
    def run(self): return '# Sanity Report\n**SANITY-001 / TEST-001 | AC-001..003**\n\n- Unit tests: simulated PASS (4/4)\n- API validation: PASS\n- Acceptance mapping: PASS\n- Overall: PASS\n- Defects: none\n'
class ReleaseAgent:
    def run(self): return '# Release Package — RELEASE-001\n**Traceability:** REQ-001, STORY-001..003, TEST-001, REVIEW-001\n\n## Release notes\nLeave submission, decision, balance, audit, and notifications PoC.\n## QA handoff / testing completed\nSanity and acceptance mapping passed.\n## Known limitations / open risks\nIn-memory generated stub; authentication and email are mocked.\n## Deployment notes\nRun Docker Compose or local setup.\n## Rollback notes\nStop containers and restore artifact JSON snapshot.\n## QA validation checklist\n- [ ] Validate happy path\n- [ ] Validate duplicate and insufficient balance\n- [ ] Verify audit trail\n'
class KnowledgeGraphAgent:
    def run(self, backlog):
        chain=[('REQ-001','Requirement'),('BRD-001','BRD'),('EPIC-001','Epic'),('STORY-001','Story'),('AC-001','Acceptance Criteria'),('CODE-001','Code'),('TEST-001','Test'),('REVIEW-001','Review'),('SANITY-001','Sanity Result'),('DEFECT-001','Defect'),('QA-001','QA Handoff'),('RELEASE-001','Release')]
        return {'nodes':[{'id':i,'type':t,'label':t+' artifact'} for i,t in chain],'edges':[{'from':chain[i][0],'to':chain[i+1][0],'relationship':['GENERATES','DECOMPOSES_TO','CONTAINS','HAS_CRITERIA','IMPLEMENTED_BY','VERIFIED_BY','REVIEWED_BY','VALIDATED_BY','PRODUCES_DEFECT_STATUS','HANDED_OFF_AS','RELEASED_AS'][i]} for i in range(len(chain)-1)]}
