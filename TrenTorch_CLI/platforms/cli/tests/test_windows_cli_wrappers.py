"""
Tests for Windows native CLI wrappers (bin/tren.cmd and bin/tren.ps1).

Ensures:
1. Native Windows wrappers exist alongside bin/tren.
2. cmd.exe can execute tren.cmd with arguments and flags, returning proper exit codes.
3. PowerShell can execute tren.ps1 with argument splatting, returning proper exit codes.
4. Non-zero exit codes propagate correctly to the calling shell.
"""

import subprocess
import sys
from pathlib import Path

import pytest


@pytest.fixture
def cli_bin_dir():
    """Return path to TrenTorch_CLI/bin directory."""
    return Path(__file__).resolve().parent.parent.parent.parent / "bin"


@pytest.fixture
def root_bin_dir():
    """Return path to repository root bin directory."""
    return Path(__file__).resolve().parent.parent.parent.parent.parent / "bin"


def test_cli_bin_wrappers_exist(cli_bin_dir):
    """Verify that tren, tren.cmd, and tren.ps1 exist in TrenTorch_CLI/bin."""
    assert (cli_bin_dir / "tren").is_file(), "bin/tren missing"
    assert (cli_bin_dir / "tren.cmd").is_file(), "bin/tren.cmd missing"
    assert (cli_bin_dir / "tren.ps1").is_file(), "bin/tren.ps1 missing"


def test_root_bin_wrappers_exist(root_bin_dir):
    """Verify that root bin forwarder wrappers exist."""
    assert (root_bin_dir / "tren").is_file(), "root bin/tren missing"
    assert (root_bin_dir / "tren.cmd").is_file(), "root bin/tren.cmd missing"
    assert (root_bin_dir / "tren.ps1").is_file(), "root bin/tren.ps1 missing"


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific wrapper tests")
def test_cmd_wrapper_execution_help(cli_bin_dir):
    """Test executing tren.cmd with --help via cmd.exe."""
    cmd_script = cli_bin_dir / "tren.cmd"
    result = subprocess.run(
        ["cmd.exe", "/c", str(cmd_script), "--help"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )
    assert result.returncode == 0, f"tren.cmd --help failed with: {result.stderr}"
    assert "Tren" in result.stdout
    assert "Available Commands" in result.stdout


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific wrapper tests")
def test_cmd_wrapper_version(cli_bin_dir):
    """Test executing tren.cmd with --version via cmd.exe."""
    cmd_script = cli_bin_dir / "tren.cmd"
    result = subprocess.run(
        ["cmd.exe", "/c", str(cmd_script), "--version"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )
    assert result.returncode == 0
    assert "Tren" in result.stdout


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific wrapper tests")
def test_cmd_wrapper_exit_code_propagation(cli_bin_dir):
    """Test that invalid command returns non-zero exit code via cmd.exe."""
    cmd_script = cli_bin_dir / "tren.cmd"
    result = subprocess.run(
        ["cmd.exe", "/c", str(cmd_script), "nonexistent_command_12345"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )
    assert result.returncode != 0


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific wrapper tests")
def test_powershell_wrapper_execution_help(cli_bin_dir):
    """Test executing tren.ps1 with --help via powershell.exe."""
    ps1_script = cli_bin_dir / "tren.ps1"
    result = subprocess.run(
        ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ps1_script), "--help"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )
    assert result.returncode == 0, f"tren.ps1 --help failed with: {result.stderr}"
    assert "Tren" in result.stdout
    assert "Available Commands" in result.stdout


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific wrapper tests")
def test_powershell_wrapper_version(cli_bin_dir):
    """Test executing tren.ps1 with --version via powershell.exe."""
    ps1_script = cli_bin_dir / "tren.ps1"
    result = subprocess.run(
        ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ps1_script), "--version"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )
    assert result.returncode == 0
    assert "Tren" in result.stdout


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific wrapper tests")
def test_powershell_wrapper_exit_code_propagation(cli_bin_dir):
    """Test that invalid command returns non-zero exit code via powershell.exe."""
    ps1_script = cli_bin_dir / "tren.ps1"
    result = subprocess.run(
        [
            "powershell.exe",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(ps1_script),
            "nonexistent_command_12345",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )
    assert result.returncode != 0


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific wrapper tests")
def test_root_forwarders_work(root_bin_dir):
    """Test executing root bin forwarders."""
    cmd_script = root_bin_dir / "tren.cmd"
    result = subprocess.run(
        ["cmd.exe", "/c", str(cmd_script), "--version"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )
    assert result.returncode == 0
    assert "Tren" in result.stdout

    ps1_script = root_bin_dir / "tren.ps1"
    result = subprocess.run(
        ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ps1_script), "--version"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )
    assert result.returncode == 0
    assert "Tren" in result.stdout
