"""
pytest data/app_data/00-python/11-errors-and-control-flow/05-assemble-job-runner/tests.py
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"00-python/11-errors-and-control-flow/{Path(__file__).resolve().parent.name}"
)
TransientError = _module.TransientError
JobFailedError = _module.JobFailedError
run_job = _module.run_job
run_jobs = _module.run_jobs


def test_success_on_first_attempt():
    log = []
    result = run_job("L", lambda: 42, 3, log)
    assert result == 42
    assert log == ["start L", "attempt 1", "end L"]


def test_transient_failures_then_success():
    calls = {"n": 0}

    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise TransientError("retry me")
        return "ok"

    log = []
    result = run_job("L", flaky, 5, log)
    assert result == "ok"
    assert log == ["start L", "attempt 1", "attempt 2", "attempt 3", "end L"]


def test_attempts_exhausted():
    def always_transient():
        raise TransientError("nope")

    log = []
    with pytest.raises(JobFailedError) as excinfo:
        run_job("L", always_transient, 3, log)
    assert excinfo.value.attempts == 3
    assert isinstance(excinfo.value.__cause__, TransientError)
    assert "end L" in log


def test_permanent_errors_are_not_retried():
    def always_fails():
        raise ValueError("bad")

    log = []
    with pytest.raises(JobFailedError) as excinfo:
        run_job("L", always_fails, 5, log)
    assert excinfo.value.attempts == 1
    assert isinstance(excinfo.value.__cause__, ValueError)
    assert log.count("attempt 1") == 1
    assert "attempt 2" not in log


def test_job_logger_does_not_suppress():
    def always_fails():
        raise ValueError("bad")

    log = []
    with pytest.raises(JobFailedError):
        run_job("L", always_fails, 1, log)
    assert "end L" in log


def test_run_jobs_isolates_failures():
    def ok():
        return "good"

    def bad():
        raise ValueError("bad")

    log = []
    result = run_jobs([("a", ok), ("b", bad), ("c", ok)], 2, log)
    assert result["results"] == {"a": "good", "c": "good"}
    assert result["failed"] == {"b": 1}


def test_else_used_for_the_return():
    log = []
    for value in (0, None, ""):
        result = run_job("L", lambda v=value: v, 1, log)
        assert result == value
