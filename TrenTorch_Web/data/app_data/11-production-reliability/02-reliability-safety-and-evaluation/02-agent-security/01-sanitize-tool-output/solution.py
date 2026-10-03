def sanitize_tool_output(output: str, forbidden_patterns: list[str]) -> str:
    sanitized = output
    for pattern in forbidden_patterns:
        if pattern:
            sanitized = sanitized.replace(pattern, "[REDACTED]")
    return sanitized
