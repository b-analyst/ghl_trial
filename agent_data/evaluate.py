"""Local check. Run this before you finish:  python /workdir/evaluate.py"""

import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "tests/test_allocate.py"], cwd=here
    )
    raise SystemExit(result.returncode)
