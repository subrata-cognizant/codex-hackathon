import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
import json,pytest
@pytest.fixture
def sample_data(): return json.loads((Path(__file__).parents[1]/'app/data/sample_dataset.json').read_text())
