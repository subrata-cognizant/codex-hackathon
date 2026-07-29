import json
from pathlib import Path
from typing import Any
class JsonRepository:
    def __init__(self, root: Path): self.root = root; root.mkdir(parents=True, exist_ok=True)
    def write_json(self, name: str, value: Any) -> Path:
        path=self.root/name; path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(value, indent=2), encoding='utf-8'); return path
    def write_text(self, name: str, value: str) -> Path:
        path=self.root/name; path.parent.mkdir(parents=True, exist_ok=True); path.write_text(value, encoding='utf-8'); return path
    def read(self, name: str) -> Any:
        path=(self.root/name).resolve()
        if self.root.resolve() not in path.parents or not path.is_file(): raise FileNotFoundError(name)
        return json.loads(path.read_text()) if path.suffix=='.json' else path.read_text()
    def list(self) -> list[str]: return sorted(str(p.relative_to(self.root)) for p in self.root.rglob('*') if p.is_file())
