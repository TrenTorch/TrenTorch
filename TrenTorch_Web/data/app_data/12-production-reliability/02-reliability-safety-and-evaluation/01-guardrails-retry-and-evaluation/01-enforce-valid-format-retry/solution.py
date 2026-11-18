def enforce_format_with_retry(
    max_retries: int, attempts: list[str], allowed_values: set[str]
) -> str:
    limit = min(len(attempts), max_retries + 1)
    for i in range(limit):
        if attempts[i].strip() in allowed_values:
            return f"SUCCESS {i + 1}"
    return f"FAILURE {limit}"
