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

    Two signals are checked, and either one is enough:

    1. ``sys.prefix != sys.base_prefix``: this Python is a venv's own
       interpreter, whether the venv was activated or its interpreter
       was run directly (``.venv/bin/python``, or the PATH entry
       ``tren setup`` adds). The Python docs call this check sufficient:
       https://docs.python.org/3/library/venv.html
    2. ``sys.real_prefix`` exists: set only by legacy ``virtualenv``
       (before 20.0), which never touched ``sys.base_prefix``.

    Precedence: none. The signals are OR'd, so either positive wins and
    neither can veto the other.

    ``VIRTUAL_ENV`` is deliberately not a signal. It only records that an
    ``activate`` script ran in this shell at some point, not which Python
    is running now, so a value left over from another project or a
    deleted venv made a system Python count as a venv (#433). The Python
    docs say it "cannot be relied upon" for this, since activating is
    optional.

    Known gap: on Python 3.10 to 3.13, ``sys.prefix`` is moved into the
    venv by the ``site`` module, so running the venv's interpreter with
    ``-S`` makes check 1 miss it. Python 3.14 sets it during path
    initialization instead, which closes the gap.

    This only inspects the current process. Whether a ``.venv`` directory
    exists on disk is a separate question, answered by callers that need
    it (see ``CLIConfig.validate``).
    """
    return sys.prefix != sys.base_prefix or hasattr(sys, "real_prefix")


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
