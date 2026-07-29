from app.agents.story_agent import StoryAgent
def test_acceptance_criteria_mapping():
 b=StoryAgent().run('BRD'); ac=b['epics'][0]['stories'][0]['acceptance_criteria'][0]; assert ac['id']=='AC-001'; assert all(ac[x] for x in ('given','when','then')); assert ac['requirement_id']=='REQ-001'
