"""
Shared, single, curriculum-wide test-only helper.

Every question's oracle solution is named `solution.py` -- the same
filename in every folder, deliberately, so each question stays
self-contained and easy to find. A previous version of this helper
lived as a separate copy inside each track directory; that worked
until more than one track's tests ran in the *same* pytest session,
at which point every copy shared the bare module name `_load` and
Python's import cache let the first-loaded track's copy silently win
for every other track's tests too (loading the wrong track's
solutions under the right-looking folder names, or failing outright
when the folder didn't exist there).

Fix: exactly one `_load.py` for the whole curriculum, and every loaded
solution is keyed by its full relative path, so two different
tracks' `01-...` folders can never collide with each other either.
"""

import importlib.util
from pathlib import Path

_DATA_DIR = Path(__file__).resolve().parent


def load_solution(relative_path: str):
    """
    relative_path: slash-separated path from data/, e.g.
    "01-classical-ml/01-linear-regression/01-hypothesis-function"
    """
    path = _DATA_DIR / relative_path / "solution.py"
    unique_name = "_solution_" + relative_path.replace("/", "_")
    spec = importlib.util.spec_from_file_location(unique_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
