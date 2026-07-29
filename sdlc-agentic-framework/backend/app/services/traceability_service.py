class TraceabilityService:
    def __init__(self, repo): self.repo=repo
    def get(self): return self.repo.read('lineage_graph.json')
