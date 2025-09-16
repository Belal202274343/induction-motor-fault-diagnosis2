#!/usr/bin/env python3
"""
Launcher for Induction Motor Fault Diagnosis - Web UI
This script starts the Flask-based web interface located at `src/webapp/app.py`.
"""

from pathlib import Path
import importlib.util
import sys


def load_flask_app() -> object:
    """Dynamically load the Flask `app` object from src/webapp/app.py.

    This avoids depending on package import paths and works when running
    `python main.py` from the repository root.
    """
    app_path = Path(__file__).parent / "src" / "webapp" / "app.py"
    if not app_path.exists():
        raise FileNotFoundError(f"Flask app not found at {app_path}")

    spec = importlib.util.spec_from_file_location("induction_webapp", str(app_path))
    module = importlib.util.module_from_spec(spec)
    # Ensure the path to repo root is on sys.path so templates/static resolution works
    sys.path.insert(0, str(Path(__file__).parent))
    spec.loader.exec_module(module)
    if not hasattr(module, "app"):
        raise AttributeError("Flask app object 'app' not found in src/webapp/app.py")
    return module.app


def main():
    app = load_flask_app()
    # Run development server by default. For production use a WSGI server (gunicorn/uvicorn).
    app.run(host="127.0.0.1", port=5000, debug=True)


if __name__ == "__main__":
    main()
