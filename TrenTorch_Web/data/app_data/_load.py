"""
Shared, curriculum-wide, test-only helper for reaching a question's solution.

A question never names where it lives. `load_solution` takes one of:

  load_solution(__file__)          the question's own solution.py, from its
                                   tests.py (the file it is called from)
  load_solution("<question name>") another question's solution.py, by the
                                   `name` in that question's README.md
                                   frontmatter (e.g. "linear-regression-mse-loss")

so folders can be renamed, renumbered, or moved between tracks without
touching any test. Names are unique across the curriculum; they are indexed
once, on the first by-name call, from the README frontmatter on disk.

Every loaded solution is keyed by its own path in the module cache, so two
questions' identically-named `solution.py` files can never collide.
"""

import importlib.util
from pathlib import Path

_DATA_DIR = Path(__file__).resolve().parent
_dirs_by_name: dict[str, list[Path]] | None = None


def _index() -> dict[str, list[Path]]:
    global _dirs_by_name
    if _dirs_by_name is None:
        _dirs_by_name = {}
        for readme in _DATA_DIR.glob("*/*/*/*/README.md"):
            with readme.open(encoding="utf-8") as handle:
                for line in handle:
                    if line.startswith("name:"):
                        _dirs_by_name.setdefault(line[5:].strip(), []).append(readme.parent)
                        break
                    if line.startswith("## "):
                        break
    return _dirs_by_name


def _resolve(ref: str) -> Path:
    if ref.endswith(".py") or "/" in ref:
        return Path(ref).resolve().parent
    found = _index().get(ref, [])
    if not found:
        raise LookupError(f"no question named {ref!r}")
    if len(found) > 1:
        raise LookupError(f"question name {ref!r} is not unique: {[str(p) for p in found]}")
    return found[0]


def load_solution(ref: str):
    folder = _resolve(ref)
    unique_name = "_solution_" + folder.relative_to(_DATA_DIR).as_posix().replace("/", "_")
    spec = importlib.util.spec_from_file_location(unique_name, folder / "solution.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
