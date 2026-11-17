def enforce_format_with_retry(
    max_retries: int, attempts: list[str], allowed_values: set[str]
) -> str:
    """
    attempts: the model's raw output text for each attempt, in order.
    allowed_values: the closed set of exactly-valid output strings (a
    fixed label set, e.g. classification labels) -- NOT a JSON-syntax
    check, a strict membership check against known-good values.

    Try attempt 1, then 2, ... up to at most max_retries + 1 total
    attempts or len(attempts) attempts, whichever is fewer, stopping at
    the first attempt whose stripped text is exactly one of
    allowed_values.

    Returns "SUCCESS i" (1-indexed) for the first valid attempt, or
    "FAILURE t" where t is the number of attempts actually tried.
    """
    # TODO: Implement the retry loop from Theory.
    pass
