from pathlib import Path
BASE_DIR=Path(__file__).resolve().parents[3]
ARTIFACT_DIR=BASE_DIR/'sample-output'
DATA_DIR=Path(__file__).resolve().parents[1]/'data'
OLLAMA_URL='http://localhost:11434/api/generate'
