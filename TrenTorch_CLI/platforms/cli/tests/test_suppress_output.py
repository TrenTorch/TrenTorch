"""Tests for suppress_output() in platforms.cli.commands.base."""

import builtins
import sys
from unittest import mock

import pytest

from platforms.cli.commands.base import suppress_output


def test_output_is_hidden(capsys):
    with suppress_output():
        print("hidden")
        print("also hidden", file=sys.stderr)

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_streams_restored_after_normal_use():
    original_stdout = sys.stdout
    original_stderr = sys.stderr

    with suppress_output():
        assert sys.stdout is not original_stdout
        assert sys.stderr is not original_stderr

    assert sys.stdout is original_stdout
    assert sys.stderr is original_stderr


def test_streams_restored_when_body_raises():
    original_stdout = sys.stdout
    original_stderr = sys.stderr

    with pytest.raises(RuntimeError):
        with suppress_output():
            raise RuntimeError("boom")

    assert sys.stdout is original_stdout
    assert sys.stderr is original_stderr


def test_first_open_failure_leaves_streams_untouched():
    original_stdout = sys.stdout
    original_stderr = sys.stderr

    with mock.patch("builtins.open", side_effect=OSError("cannot open devnull")):
        with pytest.raises(OSError):
            with suppress_output():
                pass

    assert sys.stdout is original_stdout
    assert sys.stderr is original_stderr


def test_second_open_failure_leaves_streams_untouched_and_closes_first_handle():
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    real_open = builtins.open
    opened = []

    def flaky_open(*args, **kwargs):
        if opened:
            raise OSError("cannot open devnull")
        handle = real_open(*args, **kwargs)
        opened.append(handle)
        return handle

    with mock.patch("builtins.open", side_effect=flaky_open):
        with pytest.raises(OSError):
            with suppress_output():
                pass

    assert sys.stdout is original_stdout
    assert sys.stderr is original_stderr
    assert len(opened) == 1
    assert opened[0].closed
