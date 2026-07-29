import json, urllib.request
class LocalLLMClient:
    """Optional Ollama adapter; callers always supply deterministic fallback."""
    def __init__(self, url: str, model: str='llama3.2'): self.url=url; self.model=model
    def generate(self, prompt: str, fallback: str) -> str:
        try:
            req=urllib.request.Request(self.url, data=json.dumps({'model':self.model,'prompt':prompt,'stream':False}).encode(), headers={'Content-Type':'application/json'})
            with urllib.request.urlopen(req, timeout=1) as response: return json.load(response)['response']
        except (OSError, KeyError, ValueError): return fallback
