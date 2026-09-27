"""Start the beam influence-line web application with the project environment."""

from pathlib import Path
import subprocess
import sys


if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parent
    project_python = project_dir / ".venv" / "Scripts" / "python.exe"
    python = project_python if project_python.exists() else Path(sys.executable)
    raise SystemExit(
        subprocess.call(
            [
                str(python),
                "-m",
                "uvicorn",
                "web.app:app",
                "--host",
                "127.0.0.1",
                "--port",
                "8000",
            ],
            cwd=project_dir,
        )
    )
