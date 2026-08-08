import sys
from pathlib import Path

# Prefer scripts/ on path for `import paths`; also root for `import scripts.paths`
_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_root / "scripts"))
sys.path.insert(0, str(_root))
