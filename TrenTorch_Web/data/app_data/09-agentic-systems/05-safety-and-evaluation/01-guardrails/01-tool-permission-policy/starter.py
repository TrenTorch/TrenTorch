from fnmatch import fnmatchcase


def check_permission(call: str, policy: dict) -> str:
    """Returns 'deny', 'ask' or 'allow' (deny beats ask beats allow; default deny)."""
    # TODO
    pass
