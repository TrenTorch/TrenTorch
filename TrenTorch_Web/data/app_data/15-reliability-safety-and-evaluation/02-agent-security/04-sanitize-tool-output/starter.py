def sanitize_tool_output(output: str, forbidden_patterns: list[str]) -> str:
    """Replace every occurrence of every forbidden pattern in `output` with
    "[REDACTED]", checking patterns in the order given. Return the sanitized
    string.
    """
    # TODO: implement
    pass
