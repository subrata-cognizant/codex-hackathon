from pydantic import BaseModel
class Node(BaseModel): id: str; type: str; label: str
class Edge(BaseModel):
    source: str
    target: str
    relationship: str
    def model_dump(self, *args, **kwargs):
        data = super().model_dump(*args, **kwargs); data['from'] = data.pop('source'); data['to'] = data.pop('target'); return data
class TraceabilityGraph(BaseModel): nodes: list[Node]; edges: list[Edge]
