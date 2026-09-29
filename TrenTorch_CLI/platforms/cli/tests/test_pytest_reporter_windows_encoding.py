"""Tests for Windows stream encoding configuration and ASCII-safe test reporting.

Verifies the fix for Issue:
- Stream reconfiguration to UTF-8 on Windows
- Safe ASCII divider in TrenTorchTestReporter.print_summary
- Accurate test counts extraction from pytest's terminalreporter
"""

import os
from unittest.mock import MagicMock

# Ensure conftest is importable from repo root
import conftest
from conftest import (
    TrenTorchTestReporter,
    _configure_windows_streams,
    pytest_terminal_summary,
)


def test_configure_windows_streams_on_win32():
    """Verify stdout/stderr reconfigured to utf-8 on Windows."""
    mock_stdout = MagicMock()
    mock_stderr = MagicMock()

    result = _configure_windows_streams(
        platform="win32",
        os_name="nt",
        stdout=mock_stdout,
        stderr=mock_stderr,
    )

    assert result is True
    assert os.environ.get("PYTHONIOENCODING") == "utf-8"
    mock_stdout.reconfigure.assert_called_once_with(encoding="utf-8", errors="replace")
    mock_stderr.reconfigure.assert_called_once_with(encoding="utf-8", errors="replace")


def test_configure_windows_streams_non_windows_noop():
    """Verify non-Windows platforms do not trigger stream reconfiguration."""
    mock_stdout = MagicMock()
    mock_stderr = MagicMock()

    result = _configure_windows_streams(
        platform="linux",
        os_name="posix",
        stdout=mock_stdout,
        stderr=mock_stderr,
    )

    assert result is False
    mock_stdout.reconfigure.assert_not_called()
    mock_stderr.reconfigure.assert_not_called()


def test_configure_windows_streams_tolerates_missing_reconfigure():
    """Verify streams lacking reconfigure attribute do not raise AttributeError."""

    class DummyStream:
        pass

    result = _configure_windows_streams(
        platform="win32",
        os_name="nt",
        stdout=DummyStream(),
        stderr=DummyStream(),
    )
    assert result is True


def test_reporter_print_summary_ascii_safe_separator():
    """Verify print_summary uses ASCII '=' characters instead of Unicode box-drawing characters."""
    reporter = TrenTorchTestReporter()
    reporter.use_rich = True
    reporter.console = MagicMock()
    reporter.passed = 5
    reporter.failed = 0
    reporter.skipped = 0

    reporter.print_summary()

    # Check separator printed
    printed_calls = [str(call[0][0]) for call in reporter.console.print.call_args_list if call[0]]
    assert any("=" * 50 in call_arg for call_arg in printed_calls)
    # Ensure no unicode box-drawing characters (such as \u2501)
    assert not any("\u2501" in call_arg for call_arg in printed_calls)


def test_reporter_print_summary_reads_terminalreporter_stats():
    """Verify print_summary correctly syncs counts from terminalreporter."""
    reporter = TrenTorchTestReporter()
    reporter.use_rich = True
    reporter.console = MagicMock()

    mock_terminalreporter = MagicMock()
    mock_terminalreporter.stats = {
        "passed": [MagicMock(), MagicMock(), MagicMock()],
        "failed": [MagicMock()],
        "skipped": [MagicMock(), MagicMock()],
    }

    reporter.print_summary(terminalreporter=mock_terminalreporter)

    assert reporter.passed == 3
    assert reporter.failed == 1
    assert reporter.skipped == 2

    printed_calls = [str(call[0][0]) for call in reporter.console.print.call_args_list if call[0]]
    assert any(
        "1 FAILED" in call_arg and "3 passed" in call_arg and "6 total" in call_arg
        for call_arg in printed_calls
    )


def test_pytest_terminal_summary_hook_invokes_reporter():
    """Verify pytest_terminal_summary hook delegates to _reporter with terminalreporter."""
    mock_terminalreporter = MagicMock()
    mock_config = MagicMock()
    mock_config.getoption.return_value = True

    original_print_summary = conftest._reporter.print_summary
    conftest._reporter.print_summary = MagicMock()

    try:
        pytest_terminal_summary(mock_terminalreporter, exitstatus=0, config=mock_config)
        conftest._reporter.print_summary.assert_called_once_with(mock_terminalreporter)
    finally:
        conftest._reporter.print_summary = original_print_summary
