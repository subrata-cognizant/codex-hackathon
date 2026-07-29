class ArtifactService:
    def __init__(self, repo): self.repo=repo
    def list(self): return {'artifacts':self.repo.list()}
    def get(self,name): return {'name':name,'content':self.repo.read(name)}
