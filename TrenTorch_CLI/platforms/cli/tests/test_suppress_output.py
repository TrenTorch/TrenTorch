"""Regression coverage for suppress_output stream restoration.

Opening os.devnull for stderr can fail after stdout has already been
replaced. The context manager must not leave the process pointed at a
devnull handle, and must not close the caller's real stdout/stderr.
"""

import io
import os
import sys
from unittest.mock import patch

import pytest

from platforms.cli.commands.base import suppress_output


def test_suppress_output_hides_writes_and_restores_streams():
    out = io.StringIO()
    err = io.StringIO()
    with patch.object(sys, "stdout", out), patch.object(sys, "stderr", err):
        print("visible-before", file=sys.stdout)
        with suppress_output():
            print("hidden-out")
            print("hidden-err", file=sys.stderr)
        print("visible-after", file=sys.stdout)
        print("visible-err", file=sys.stderr)
        assert sys.stdout is out
        assert sys.stderr is err
        assert not out.closed
        assert not err.closed

    assert "hidden-out" not in out.getvalue()
    assert "hidden-err" not in err.getvalue()
    assert "visible-before" in out.getvalue()
    assert "visible-after" in out.getvalue()
    assert "visible-err" in err.getvalue()


def test_suppress_output_restores_streams_when_stderr_devnull_open_fails():
    out = io.StringIO()
    err = io.StringIO()
    real_open = open
    calls = {"n": 0}

    def flaky_open(path, mode="r", *args, **kwargs):
        if path == os.devnull:
            calls["n"] += 1
            if calls["n"] == 2:
                raise OSError("too many open files")
        return real_open(path, mode, *args, **kwargs)

    with patch.object(sys, "stdout", out), patch.object(sys, "stderr", err):
        with patch("platforms.cli.commands.base.open", flaky_open):
            with pytest.raises(OSError, match="too many open files"):
                with suppress_output():
                    print("should-not-run")
        assert sys.stdout is out
        assert sys.stderr is err
        assert not out.closed
        assert not err.closed
        print("still-works", file=sys.stdout)
        print("still-err", file=sys.stderr)

    assert "should-not-run" not in out.getvalue()
    assert "still-works" in out.getvalue()
    assert "still-err" in err.getvalue()


def test_suppress_output_restores_streams_when_stdout_devnull_open_fails():
    out = io.StringIO()
    err = io.StringIO()

    def failing_open(path, mode="r", *args, **kwargs):
        if path == os.devnull:
            raise OSError("devnull unavailable")
        return open(path, mode, *args, **kwargs)

    with patch.object(sys, "stdout", out), patch.object(sys, "stderr", err):
        with patch("platforms.cli.commands.base.open", failing_open):
            with pytest.raises(OSError, match="devnull unavailable"):
                with suppress_output():
                    print("should-not-run")
        assert sys.stdout is out
        assert sys.stderr is err
        assert not out.closed
        assert not err.closed
