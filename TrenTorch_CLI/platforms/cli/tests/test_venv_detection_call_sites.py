"""
Regression tests for issue #433: the companion server's /api/status and the
TUI health tab used their own venv check (sys.prefix != sys.base_prefix or
VIRTUAL_ENV) that ignored sys.real_prefix, so they could disagree with
main.py's guard. Both now call is_venv_active(); these pin the case each
old copy got wrong, plus the plain "no venv" case.
"""

import asyncio
import sys

import pytest

from platforms.cli.core.config import CLIConfig
from platforms.cli.server.handler import TrenTorchRequestHandler


def _only_real_prefix(monkeypatch):
    monkeypatch.delenv("VIRTUAL_ENV", raising=False)
    monkeypatch.setattr(sys, "prefix", "/fake/same")
    monkeypatch.setattr(sys, "base_prefix", "/fake/same")
    monkeypatch.setattr(sys, "real_prefix", "/fake/old-venv", raising=False)


def _no_signal(monkeypatch):
    monkeypatch.delenv("VIRTUAL_ENV", raising=False)
    monkeypatch.setattr(sys, "prefix", "/fake/same")
    monkeypatch.setattr(sys, "base_prefix", "/fake/same")
    monkeypatch.delattr(sys, "real_prefix", raising=False)


def _server_in_venv(tmp_path):
    """Call the real _handle_get_status without starting an HTTP server."""
    handler = object.__new__(TrenTorchRequestHandler)
    handler.config = CLIConfig.from_project_root(tmp_path)
    handler._load_progress = lambda: {}
    handler._all_module_numbers = lambda: ("01",)
    sent = {}
    handler._send_json = lambda data, status=None: sent.update(data)
    handler._handle_get_status()
    return sent["in_venv"]


def test_server_status_counts_real_prefix_as_venv(monkeypatch, tmp_path):
    _only_real_prefix(monkeypatch)
    assert _server_in_venv(tmp_path) is True


def test_server_status_reports_no_venv_without_any_signal(monkeypatch, tmp_path):
    _no_signal(monkeypatch)
    assert _server_in_venv(tmp_path) is False


def _tui_health_summary():
    pytest.importorskip("textual")
    from platforms.cli.tui.app import TrenTorchApp

    async def _runner():
        app = TrenTorchApp(config=CLIConfig.from_project_root(), initial_module="01")
        captured = []
        async with app.run_test() as pilot:
            await pilot.pause()
            summary = app.query_one("#health-summary-text")
            original = summary.update

            def _record(content="", *args, **kwargs):
                captured.append(str(content))
                return original(content, *args, **kwargs)

            summary.update = _record
            app._update_health_tab()
        return captured[-1]

    return asyncio.run(_runner())


def test_tui_health_tab_counts_real_prefix_as_venv(monkeypatch):
    _only_real_prefix(monkeypatch)
    assert "Active Virtualenv" in _tui_health_summary()


def test_tui_health_tab_reports_system_python_without_any_signal(monkeypatch):
    _no_signal(monkeypatch)
    assert "System Python" in _tui_health_summary()
