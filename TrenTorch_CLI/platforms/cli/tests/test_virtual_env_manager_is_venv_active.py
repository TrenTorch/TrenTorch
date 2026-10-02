"""
MC/DC coverage for is_venv_active(), the single venv-detection helper
shared by main.py's CLI-entry guard and CLIConfig.validate() (issue #348:
those two used to carry separate, disagreeing copies of this check).

3 atoms, OR'd: VIRTUAL_ENV env var, sys.prefix != sys.base_prefix, and
sys.real_prefix. A "none" baseline plus each atom flipped alone.
"""

import sys

from platforms.cli.core.virtual_env_manager import is_venv_active


def _set_signals(monkeypatch, *, venv_var, differing_prefix, real_prefix):
    if venv_var:
        monkeypatch.setenv("VIRTUAL_ENV", "/fake/venv")
    else:
        monkeypatch.delenv("VIRTUAL_ENV", raising=False)

    if differing_prefix:
        monkeypatch.setattr(sys, "prefix", "/fake/venv")
        monkeypatch.setattr(sys, "base_prefix", "/fake/system")
    else:
        monkeypatch.setattr(sys, "prefix", "/fake/same")
        monkeypatch.setattr(sys, "base_prefix", "/fake/same")

    if real_prefix:
        monkeypatch.setattr(sys, "real_prefix", "/fake/old-venv", raising=False)
    else:
        monkeypatch.delattr(sys, "real_prefix", raising=False)


def test_no_signal_is_not_a_venv(monkeypatch):
    """Baseline: all three False -> False."""
    _set_signals(monkeypatch, venv_var=False, differing_prefix=False, real_prefix=False)
    assert is_venv_active() is False


def test_virtual_env_var_alone_is_a_venv(monkeypatch):
    """Activated venv (or a stale VIRTUAL_ENV) with a system interpreter:
    the env var alone is enough -- the documented "positive wins" rule."""
    _set_signals(monkeypatch, venv_var=True, differing_prefix=False, real_prefix=False)
    assert is_venv_active() is True


def test_differing_prefix_alone_is_a_venv(monkeypatch):
    """Venv interpreter run directly without activating (no VIRTUAL_ENV):
    the prefix mismatch alone is enough."""
    _set_signals(monkeypatch, venv_var=False, differing_prefix=True, real_prefix=False)
    assert is_venv_active() is True


def test_real_prefix_alone_is_a_venv(monkeypatch):
    """Legacy virtualenv (< 20.0) only sets sys.real_prefix."""
    _set_signals(monkeypatch, venv_var=False, differing_prefix=False, real_prefix=True)
    assert is_venv_active() is True


def test_venv_directory_on_disk_does_not_count(monkeypatch, tmp_path):
    """A .venv directory existing is not a process-level signal; only
    CLIConfig.validate() layers that check on top of this helper."""
    (tmp_path / ".venv").mkdir()
    monkeypatch.chdir(tmp_path)
    _set_signals(monkeypatch, venv_var=False, differing_prefix=False, real_prefix=False)
    assert is_venv_active() is False
