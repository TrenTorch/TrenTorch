def check_hash_mode(requirements: list[dict]) -> list[str]:
    """
    Each requirement is a dict with keys "name", "spec" (e.g. "==1.2.3",
    ">=2.0", or "") and "hashes" (a possibly empty list of strings).

    Hash-checking mode is ACTIVE if at least one requirement has a
    non-empty "hashes" list. If it is not active, return [].

    If it is active, every requirement must be:
      - pinned: its spec starts with "==" and contains no "*"
      - hashed: its "hashes" list is non-empty
    Return one error string per violation, in the form
      "<name>: not pinned"   or   "<name>: missing hash"
    ordered by requirement name, and for one requirement "not pinned"
    before "missing hash". Return [] when there are no violations.
    """
    # TODO: implement this, see the Theory tab for the rules.
    pass
