import subprocess
import sys
from pathlib import Path


project_root = Path(__file__).parent.resolve()

main_script = project_root / "Agent Dashboard.py"
# Run Streamlit as a subprocess
subprocess.run(
    [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(main_script),
        "--server.address=127.0.0.1",
    ],
    cwd=project_root,
)
