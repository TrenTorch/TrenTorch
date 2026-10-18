"""
Coverage for atomic_io.read_json_or_warn -- the read-side companion to
atomic_write_json.

Found by direct audit ("errors should never go silent"): every progress.json
/ milestones.json read site in the CLI caught a corrupted or unreadable
file with a bare `except (OSError, json.JSONDecodeError): pass` and
silently fell back to an empty default. A student whose real progress.json
exists on disk but fails to parse (a manual edit gone wrong, a disk error,
an old pre-atomic-write crash) just sees "0/20 modules complete" with zero
indication their actual data might still be sitting right there,
unreadable -- indistinguishable from genuinely having no progress.

read_json_or_warn() keeps the same "don't crash the CLI" behavior (still
returns the default) but prints exactly what happened and where, so the
user finds out why their progress looks wrong instead of assuming it's
gone.
"""

import json
import subprocess
import sys
from io import StringIO

from rich.console import Console

from platforms.cli.core.atomic_io import read_json_or_warn
from platforms.cli.core.state_schema import validate_milestones, validate_progress


def _run_tren(args, cwd):
    result = subprocess.run(
        [sys.executable, "-m", "platforms.cli.main", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
    )
    return result.returncode, result.stdout or "", result.stderr or ""


def test_milestone_status_does_not_crash_on_list_progress(tmp_path):
    """CLI-level: `tren milestone status` with [] in progress.json must
    warn and continue, not traceback (issue #503)."""
    project = tmp_path / "project"
    user_data = project / "user_data"
    user_data.mkdir(parents=True)
    (user_data / "progress.json").write_text("[]", encoding="utf-8")

    code, out, err = _run_tren(["milestone", "status"], cwd=project)
    combined = out + err

    assert "Traceback" not in combined, combined
    assert "AttributeError" not in combined, combined
    assert "expected format" in combined, combined


def test_missing_file_returns_default_silently(tmp_path):
    """A file that was never created (first run, nothing saved yet) is a
    completely normal case -- no warning, just the default."""
    target = tmp_path / "progress.json"
    buf = StringIO()
    console = Console(file=buf, width=120, no_color=True)

    result = read_json_or_warn(target, {"completed_modules": []}, console=console)

    assert result == {"completed_modules": []}
    assert buf.getvalue() == ""


def test_valid_file_returns_its_real_content(tmp_path):
    target = tmp_path / "progress.json"
    target.write_text(json.dumps({"completed_modules": ["01", "02", "03"]}), encoding="utf-8")
    buf = StringIO()
    console = Console(file=buf, width=120, no_color=True)

    result = read_json_or_warn(target, {}, console=console)

    assert result == {"completed_modules": ["01", "02", "03"]}
    assert buf.getvalue() == ""


def test_corrupted_file_warns_and_returns_default(tmp_path):
    """The actual regression: a file that exists but fails to parse must
    warn, not silently pretend it was never there."""
    target = tmp_path / "progress.json"
    target.write_text('{"completed_modules": ["01", "02"', encoding="utf-8")  # truncated JSON
    buf = StringIO()
    console = Console(file=buf, width=120, no_color=True)

    result = read_json_or_warn(
        target, {"completed_modules": []}, console=console, label="Your saved progress"
    )
    out = buf.getvalue()

    assert result == {"completed_modules": []}
    assert "Your saved progress" in out
    assert "couldn't be read" in out
    assert str(target) in out


def test_corrupted_file_path_is_not_word_wrapped(tmp_path):
    """A long enough path must not get reflowed mid-word to fit the
    console's width. Found live in CI: a Windows runner's deeply nested
    temp directory pushed 'File: <path>' past a default-width console,
    and Rich wrapped it right through the middle of the filename --
    corrupting the one piece of information (where's the broken file?)
    this whole warning exists to hand the user. Forcing a narrow console
    width here reproduces that deterministically, independent of however
    long any given OS's actual temp path happens to be."""
    nested = tmp_path / "a_deeply" / "nested" / "temp" / "directory" / "structure" / "like_ci_uses"
    nested.mkdir(parents=True)
    target = nested / "progress.json"
    target.write_text('{"a": 1', encoding="utf-8")  # truncated JSON

    buf = StringIO()
    console = Console(file=buf, width=40, no_color=True)  # narrow enough to force a wrap

    read_json_or_warn(target, {}, console=console, label="Your saved progress")
    out = buf.getvalue()

    assert str(target) in out, f"path got wrapped/split across lines:\n{out}"
    # The user needs to know what to actually do, not just that
    # something went wrong.
    assert "back it up" in out.lower()


def test_corrupted_file_without_console_warns_to_stderr(tmp_path, capsys):
    """Read sites with no Rich console handy (e.g. an HTTP request
    handler) must still surface the warning somewhere, not swallow it."""
    target = tmp_path / "progress.json"
    target.write_text("not json at all", encoding="utf-8")

    result = read_json_or_warn(target, {}, label="Your saved progress")
    captured = capsys.readouterr()

    assert result == {}
    assert "Your saved progress" in captured.err
    assert "couldn't be read" in captured.err


def test_validate_progress_rejects_list_root():
    assert validate_progress([]) is None


def test_validate_progress_rejects_scalar_root():
    assert validate_progress("hello") is None
    assert validate_progress(None) is None


def test_validate_progress_resets_null_list_field_keeps_valid_ones():
    data, repaired = validate_progress({"started_modules": None, "completed_modules": ["01"]})
    assert data["started_modules"] == []
    assert data["completed_modules"] == ["01"]
    assert repaired == ["started_modules"]  # only the present-but-wrong field


def test_validate_progress_resets_string_field():
    data, repaired = validate_progress({"completed_modules": "01"})
    assert data["completed_modules"] == []
    assert repaired == ["completed_modules"]


def test_validate_milestones_resets_bad_fields():
    data, repaired = validate_milestones(
        {
            "completed_milestones": None,
            "unlocked_milestones": "01",
            "unlock_dates": None,
            "total_unlocked": "3",
        }
    )
    assert data["completed_milestones"] == []
    assert data["unlocked_milestones"] == []
    assert data["unlock_dates"] == {}
    assert data["total_unlocked"] == 0
    assert set(repaired) == {
        "completed_milestones",
        "unlocked_milestones",
        "unlock_dates",
        "total_unlocked",
    }


def test_validate_progress_leaves_missing_keys_alone():
    """A valid file that predates a field must not be mutated: missing
    keys are left alone (callers handle them with .get(key, default)),
    and nothing is reported as repaired. Filling them in here would get
    written back to the user's file on the next save."""
    data, repaired = validate_progress({"started_modules": ["01"], "completed_modules": []})
    assert data["started_modules"] == ["01"]
    assert data["completed_modules"] == []
    assert "completion_dates" not in data  # NOT filled in
    assert repaired == []


def test_read_json_or_warn_list_root_warns_expected_format(tmp_path):
    target = tmp_path / "progress.json"
    target.write_text("[]", encoding="utf-8")
    buf = StringIO()
    console = Console(file=buf, width=120, no_color=True)

    result = read_json_or_warn(
        target,
        {"started_modules": []},
        console=console,
        label="Your saved progress",
        validate=validate_progress,
    )
    out = buf.getvalue()

    assert result == {"started_modules": []}
    assert "expected format" in out
    assert "couldn't be read" not in out
    assert str(target) in out
