"""Module entry point so ``python -m twlegalrag`` works.

Needed for installs where the ``twlegalrag`` console script is not on PATH —
notably ``pip install --user`` on Windows, where the user Scripts directory is
often missing from PATH. ``skills/tw-legal-rag/scripts/search_judgments.py``
falls back to ``[sys.executable, "-m", "twlegalrag"]`` for exactly that case.
"""

from .cli import app

if __name__ == "__main__":
    app()
