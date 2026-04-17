"""pytest configuration — adds src/ to the Python path for imports."""

import sys
from pathlib import Path

# Allow importing `victor` from the src layout during tests
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
