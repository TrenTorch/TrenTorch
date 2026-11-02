"""
Regression tests for the ref `tren system update` clones (#661).
"""

import subprocess

import pytest

from platforms.cli.cli_platform.system import update as update_module
from platforms.cli.cli_platform.system.update import UpdateCommand
from platforms.cli.core.config import CLIConfig


def test_clone_uses_configured_branch(tmp_path, monkeypatch):
    calls = []

    def fake_run(args, **kwargs):
        calls.append(args)
        return subprocess.CompletedProcess(args, 1, "", "stop after clone")

    monkeypatch.setattr(update_module.subprocess, "run", fake_run)
    cmd = UpdateCommand(CLIConfig.from_project_root(tmp_path))

    assert cmd._run_update(UpdateCommand.BRANCH) is False
    clone = calls[0]
    assert clone[:2] == ["git", "clone"]
    assert clone[clone.index("--branch") + 1] == UpdateCommand.BRANCH


@pytest.mark.slow
def test_configured_branch_exists_on_remote():
    result = subprocess.run(
        ["git", "ls-remote", "--exit-code", "--heads", UpdateCommand.REPO_URL, UpdateCommand.BRANCH],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, f"{UpdateCommand.BRANCH!r} not found on {UpdateCommand.REPO_URL}"
