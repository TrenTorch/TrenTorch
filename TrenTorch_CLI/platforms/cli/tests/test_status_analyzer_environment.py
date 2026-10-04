"""
MC/DC coverage for TrenTorchStatusAnalyzer.check_environment()'s venv-detection
decision.

check_environment() now delegates to is_venv_active() (issue #433), the
same helper main.py's guard uses, so the decision is the helper's: any of
VIRTUAL_ENV set, sys.prefix != sys.base_prefix, or sys.real_prefix. Before
#433 the analyzer had its own copy that ignored VIRTUAL_ENV, so it could
disagree with the guard.

Each case pins all three signals via monkeypatch (never relying on
whatever venv state pytest happens to be running under, including a
VIRTUAL_ENV inherited from the shell or CI): a "none" baseline plus each
signal flipped alone. sys.base_prefix itself is never deleted: it exists on
every Python since 3.3 and TrenTorch requires 3.10+.
"""

import sys

from platforms.cli.core.status_analyzer import TrenTorchStatusAnalyzer


def _virtual_env_active(monkeypatch, tmp_path, *, venv_var, differing_prefix, real_prefix):
    if venv_var:
        monkeypatch.setenv("VIRTUAL_ENV", "/fake/venv")
    else:
        monkeypatch.delenv("VIRTUAL_ENV", raising=False)

    if differing_prefix:
        monkeypatch.setattr(sys, "prefix", "/fake/venv")
        monkeypatch.setattr(sys, "base_prefix", "/fake/base")
    else:
        monkeypatch.setattr(sys, "prefix", "/fake/same-path")
        monkeypatch.setattr(sys, "base_prefix", "/fake/same-path")

    if real_prefix:
        monkeypatch.setattr(sys, "real_prefix", "/fake/system-python", raising=False)
    else:
        monkeypatch.delattr(sys, "real_prefix", raising=False)

    return TrenTorchStatusAnalyzer(repo_path=tmp_path).check_environment()["virtual_env_active"]


def test_no_signal_is_false(monkeypatch, tmp_path):
    """Baseline: all three signals False -> False."""
    result = _virtual_env_active(
        monkeypatch, tmp_path, venv_var=False, differing_prefix=False, real_prefix=False
    )
    assert result is False


def test_virtual_env_var_alone_is_true(monkeypatch, tmp_path):
    """Only VIRTUAL_ENV differs from the baseline -> True. This is the
    case the analyzer's old copy got wrong (it ignored VIRTUAL_ENV)."""
    result = _virtual_env_active(
        monkeypatch, tmp_path, venv_var=True, differing_prefix=False, real_prefix=False
    )
    assert result is True


def test_differing_prefix_alone_is_true(monkeypatch, tmp_path):
    """Only sys.prefix != sys.base_prefix differs from the baseline -> True."""
    result = _virtual_env_active(
        monkeypatch, tmp_path, venv_var=False, differing_prefix=True, real_prefix=False
    )
    assert result is True


def test_real_prefix_alone_is_true(monkeypatch, tmp_path):
    """Only sys.real_prefix differs from the baseline -> True."""
    result = _virtual_env_active(
        monkeypatch, tmp_path, venv_var=False, differing_prefix=False, real_prefix=True
    )
    assert result is True


def test_inactive_venv_is_reported_as_an_issue(monkeypatch, tmp_path):
    """The False branch also records the issue string the analyzer's
    summary panel shows."""
    monkeypatch.delenv("VIRTUAL_ENV", raising=False)
    monkeypatch.setattr(sys, "prefix", "/fake/same-path")
    monkeypatch.setattr(sys, "base_prefix", "/fake/same-path")
    monkeypatch.delattr(sys, "real_prefix", raising=False)

    env = TrenTorchStatusAnalyzer(repo_path=tmp_path).check_environment()

    assert "Virtual environment not activated" in env["issues"]
