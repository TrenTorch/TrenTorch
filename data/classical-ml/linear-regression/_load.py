"""
Test-only helper for this track.

Every question folder's oracle solution is named `solution.py` -- the
same filename in every folder, deliberately, so each question stays
self-contained and easy to find. That means a plain `import solution`
would collide the moment two questions' tests run in the same process
(Python caches modules by name, so only the first "solution" ever
loaded would win -- silently testing the wrong question's code).

`load_solution(question_folder)` sidesteps that by loading each
solution.py under a unique internal module name
(`_solution_<question_folder>`), keyed off the folder it actually came
from. Never imported by student-facing code or by the build script --
only by a later question's tests.py, to reuse an earlier question's
function instead of repeating it.
"""

import importlib.util
from pathlib import Path

_TRACK_DIR = Path(__file__).resolve().parent


def load_solution(question_folder: str):
    path = _TRACK_DIR / question_folder / "solution.py"
    spec = importlib.util.spec_from_file_location(f"_solution_{question_folder}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
