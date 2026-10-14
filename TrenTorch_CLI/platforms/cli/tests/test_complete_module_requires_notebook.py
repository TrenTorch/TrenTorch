"""complete_module must refuse a module whose notebook was never created, even with --skip-* flags."""

from io import StringIO

import pytest
from rich.console import Console

import platforms.cli.processes.module_workflow.workflow as workflow_module
from platforms.cli.core.config import CLIConfig
from platforms.cli.processes.module_workflow.workflow import ModuleWorkflowCommand


@pytest.fixture
def workflow(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("TREN_DEV_VERIFY_SOLUTION", raising=False)
    monkeypatch.setattr(workflow_module, "get_module_mapping", lambda: {"01": "01_tensor"})
    cmd = ModuleWorkflowCommand(CLIConfig.from_project_root(tmp_path))
    cmd.console = Console(file=StringIO(), width=200, no_color=True)
    return cmd


@pytest.mark.parametrize("skip_tests,skip_export", [(False, False), (True, False), (True, True)])
def test_unstarted_module_is_not_completed(workflow, skip_tests, skip_export):
    rc = workflow.complete_module("01", skip_tests=skip_tests, skip_export=skip_export)

    assert rc == 1
    assert "not started yet" in workflow.console.file.getvalue()
    assert "tren module start 01" in workflow.console.file.getvalue()
    assert not workflow.is_module_completed("01")
