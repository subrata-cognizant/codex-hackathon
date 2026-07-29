from app.agents.knowledge_graph_agent import KnowledgeGraphAgent
def test_traceability_graph_creation():
 g=KnowledgeGraphAgent().run({}); ids={n['id'] for n in g['nodes']}; assert {'REQ-001','BRD-001','CODE-001','TEST-001','RELEASE-001'}<=ids; assert all('from' in e and 'to' in e for e in g['edges'])
