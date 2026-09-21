"""
Small text helpers for CLI output.
"""


def pluralize(word: str, count: int) -> str:
    """Return `word` in its singular or plural form for `count`.

    Only the regular "+s" plural is handled, which covers every noun the
    CLI currently counts (day, hour, minute, module, change). Pass the
    singular form; irregular nouns need their own handling.

        >>> f"{1} {pluralize('day', 1)} ago"
        '1 day ago'
        >>> f"{3} {pluralize('day', 3)} ago"
        '3 days ago'
    """
    return word if count == 1 else f"{word}s"
