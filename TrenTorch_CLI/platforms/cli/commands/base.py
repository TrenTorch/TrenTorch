"""
Base command class for TrenTorch CLI.
"""

import logging
import os
import sys
from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace
from contextlib import contextmanager
from pathlib import Path

from ..core.config import CLIConfig
from ..core.console import get_console
from ..core.exceptions import TrenTorchCLIError
from ..core.virtual_env_manager import get_venv_path

logger = logging.getLogger(__name__)


@contextmanager
def suppress_output():
    """Context manager to suppress stdout and stderr temporarily.

    Both devnull handles are opened before either stream is replaced. If
    opening the second handle fails, the original streams are left untouched
    and the first handle is closed. Cleanup restores the original streams
    before closing the devnull handles, so a failure cannot close the real
    stdout or stderr.
    """
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    devnull_out = None
    devnull_err = None
    try:
        devnull_out = open(os.devnull, "w")
        devnull_err = open(os.devnull, "w")
        sys.stdout = devnull_out
        sys.stderr = devnull_err
        yield
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        if devnull_out is not None:
            devnull_out.close()
        if devnull_err is not None:
            devnull_err.close()


class BaseCommand(ABC):
    """Base class for all CLI commands."""

    # Command metadata - override in subclasses
    category: str = "other"  # "essential", "workflow", "tracking", "community", "shortcut", "developer"
    hidden: bool = False  # Set to True to hide from main help

    def __init__(self, config: CLIConfig):
        """Initialize the command with configuration."""
        self.config = config
        self.console = get_console()

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the command name."""
        pass

    @property
    def venv_path(self) -> Path:
        """Return the command name."""
        return get_venv_path()

    @property
    @abstractmethod
    def description(self) -> str:
        """Return the command description."""
        pass

    @abstractmethod
    def add_arguments(self, parser: ArgumentParser) -> None:
        """Add command-specific arguments to the parser."""
        pass

    @abstractmethod
    def run(self, args: Namespace) -> int:
        """Execute the command and return exit code."""
        pass

    def validate_args(self, args: Namespace) -> None:
        """Validate command arguments. Override in subclasses if needed."""
        pass

    def execute(self, args: Namespace) -> int:
        """Execute the command with error handling."""
        try:
            self.validate_args(args)
            return self.run(args)
        except TrenTorchCLIError as e:
            logger.error(f"Command failed: {e}")
            self.console.print(f"[red]❌ {e}[/red]")
            return 1
        except Exception as e:
            logger.exception(f"Unexpected error in command {self.name}")
            self.console.print(f"[red]❌ Unexpected error: {e}[/red]")
            return 1
