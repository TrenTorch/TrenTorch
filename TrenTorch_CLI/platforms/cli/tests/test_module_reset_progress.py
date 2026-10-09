"""Progress tracking through the single-module and all-module reset commands."""

import json
from argparse import Namespace
from datetime import datetime
from io import StringIO
from unittest.mock import Mock

import pytest
from rich.console import Console

from platforms.cli.core import atomic_io
from platforms.cli.core.config import CLIConfig
from platforms.cli.processes.module_workflow import reset


@pytest.fixture
def reset_command(tmp_path, monkeypatch):
    modules = {"01": "01_tensor", "02": "02_activations"}
    for name in modules.values():
        (tmp_path / "data" / "src" / name).mkdir(parents=True)
    monkeypatch.setattr(reset, "get_module_mapping", lambda: modules.copy())
    converter = Mock(return_value=True)
    monkeypatch.setattr(reset, "convert_py_to_notebook", converter)
    output = StringIO()
    command = reset.ModuleResetCommand(CLIConfig.from_project_root(tmp_path))
    command.console = Console(file=output, width=160, no_color=True)
    return command, converter, output


def _run(command, *, all_modules=False, force=True):
    return command.run(Namespace(module_number="1", all=all_modules, force=force))


def _read_progress(tmp_path):
    return json.loads((tmp_path / "user_data" / "progress.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("all_modules", [False, True], ids=["single", "all"])
def test_reset_creates_missing_progress(tmp_path, reset_command, all_modules):
    command, converter, output = reset_command
    before = datetime.now()

    assert _run(command, all_modules=all_modules) == 0

    progress = _read_progress(tmp_path)
    assert before <= datetime.fromisoformat(progress.pop("last_updated")) <= datetime.now()
    assert progress == {
        "version": "1.0",
        "started_modules": [],
        "completed_modules": [],
        "last_worked": None,
    }
    assert converter.call_count == (2 if all_modules else 1)
    assert (tmp_path / "user_data" / "milestones.json").exists() == all_modules
    assert "Could not save" not in output.getvalue()


@pytest.mark.parametrize("all_modules", [False, True], ids=["single", "all"])
def test_reset_preserves_its_progress_scope(tmp_path, reset_command, all_modules):
    command, _, _ = reset_command
    user_data = tmp_path / "user_data"
    user_data.mkdir()
    original = {
        "version": "1.0",
        "started_modules": ["01", "02"],
        "completed_modules": ["01", "02"],
        "last_worked": "02",
        "last_updated": "2000-01-01T00:00:00",
        "notes": {"02": "Keep my notes"},
    }
    (user_data / "progress.json").write_text(json.dumps(original), encoding="utf-8")
    milestones = user_data / "milestones.json"
    milestones.write_text('{"completed_milestones": ["01"], "notes": "keep"}\n', encoding="utf-8")
    saved_milestones = milestones.read_bytes()

    assert _run(command, all_modules=all_modules) == 0

    progress = _read_progress(tmp_path)
    assert progress.pop("last_updated") != original.pop("last_updated")
    if all_modules:
        assert progress == {
            "version": "1.0",
            "started_modules": [],
            "completed_modules": [],
            "last_worked": None,
        }
        assert json.loads(milestones.read_text(encoding="utf-8")) == {
            "version": "1.0",
            "completed_milestones": [],
            "completion_dates": {},
        }
    else:
        assert progress == {**original, "started_modules": ["02"], "completed_modules": ["02"]}
        assert milestones.read_bytes() == saved_milestones


@pytest.mark.parametrize("existing_progress", [False, True], ids=["missing", "existing"])
def test_failed_single_reset_does_not_write_progress(tmp_path, reset_command, existing_progress):
    command, converter, _ = reset_command
    converter.return_value = False
    progress_file = tmp_path / "user_data" / "progress.json"
    original = '{"completed_modules": ["01", "02"]}\n'
    if existing_progress:
        progress_file.parent.mkdir()
        progress_file.write_text(original, encoding="utf-8")

    assert _run(command) == 1

    assert progress_file.exists() == existing_progress
    if existing_progress:
        assert progress_file.read_text(encoding="utf-8") == original


def test_single_reset_still_warns_about_corrupted_progress(tmp_path, reset_command):
    command, _, output = reset_command
    progress_file = tmp_path / "user_data" / "progress.json"
    progress_file.parent.mkdir()
    progress_file.write_text('{"completed_modules": [', encoding="utf-8")

    assert _run(command) == 0

    assert "Your saved progress exists but couldn't be read" in output.getvalue()
    assert str(progress_file) in output.getvalue()
    assert set(_read_progress(tmp_path)) == {"last_updated"}


@pytest.mark.parametrize("existing_progress", [False, True], ids=["missing", "existing"])
def test_single_reset_warns_when_atomic_save_fails(tmp_path, reset_command, monkeypatch, existing_progress):
    command, _, output = reset_command
    progress_file = tmp_path / "user_data" / "progress.json"
    original = '{"completed_modules": ["01", "02"]}\n'
    if existing_progress:
        progress_file.parent.mkdir()
        progress_file.write_text(original, encoding="utf-8")
    monkeypatch.setattr(atomic_io.os, "replace", Mock(side_effect=OSError("disk unavailable")))

    assert _run(command) == 0

    assert "Could not save progress.json: disk unavailable" in output.getvalue()
    assert progress_file.exists() == existing_progress
    if existing_progress:
        assert progress_file.read_text(encoding="utf-8") == original
    assert list(progress_file.parent.glob(".progress.json.*.tmp")) == []


def test_cancelled_single_reset_does_not_create_progress(tmp_path, reset_command, monkeypatch):
    command, converter, _ = reset_command
    monkeypatch.setattr("builtins.input", lambda _: "n")

    assert _run(command, force=False) == 0

    converter.assert_not_called()
    assert not (tmp_path / "user_data" / "progress.json").exists()
