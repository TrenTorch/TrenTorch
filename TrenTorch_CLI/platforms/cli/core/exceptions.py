"""
Exception hierarchy for TrenTorch CLI.

The CLI uses a single ``TrenTorchCLIError`` type for anticipated failures so
call sites stay simple and ``except`` clauses never shadow Python builtins such
as ``EnvironmentError`` or ``ModuleNotFoundError``.
"""


class TrenTorchCLIError(Exception):
    """Base exception for all anticipated CLI errors."""

    pass
