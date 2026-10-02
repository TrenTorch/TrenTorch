import json
import os
import sys
from pathlib import Path

DEFAULT_VENV = ".venv"
CONFIG_FILE = "maintainer_use/.tinyrc"


def get_venv_bin_dir(venv_path: Path) -> Path:
    """Return the bin directory for a venv (Scripts/ on Windows, bin/ on Unix)."""
    if sys.platform == "win32" or os.name == "nt":
        return venv_path / "Scripts"
    return venv_path / "bin"


def is_venv_active() -> bool:
    """Return True if the running interpreter belongs to a virtual environment.

    Three signals are checked, and any one of them is enough:

    1. ``VIRTUAL_ENV`` is set: the venv was activated (the ``activate``
       script, or a tool like direnv that does the same).
    2. ``sys.prefix != sys.base_prefix``: this Python is a venv's own
       interpreter, even when run directly as ``.venv/bin/python``
       without activating.
    3. ``sys.real_prefix`` exists: set only by legacy ``virtualenv``
       (before 20.0), which never touched ``sys.base_prefix``.

    Precedence: none. The signals are OR'd, so any single positive wins
    and no signal can veto another. The cost is that a stale
    ``VIRTUAL_ENV`` left in the shell makes a system Python count as
    active. Requiring every signal to agree would be worse: the PATH
    entry ``tren setup`` adds runs the venv's interpreter without
    activating it, so ``VIRTUAL_ENV`` is unset on the path the README
    recommends, and every one of those students would be blocked.

    This only inspects the current process. Whether a ``.venv`` directory
    exists on disk is a separate question, answered by callers that need
    it (see ``CLIConfig.validate``).
    """
    return (
        os.environ.get("VIRTUAL_ENV") is not None
        or sys.prefix != sys.base_prefix
        or hasattr(sys, "real_prefix")
    )


def get_venv_path() -> Path:
    """
    Fetch venv in case users have a custom path
    """
    # print(f"running this from {os.getcwd()}")  # Debug output - commented out for clean CLI
    if "VENV_PATH" in os.environ:
        return Path(os.environ["VENV_PATH"]).expanduser().resolve()

    if Path(CONFIG_FILE).exists():
        try:
            with open(CONFIG_FILE, encoding="utf-8") as f:
                cfg = json.load(f)
            return Path(cfg.get("venv_path", DEFAULT_VENV)).expanduser().resolve()
        except Exception:
            pass

    return Path(DEFAULT_VENV).resolve()
