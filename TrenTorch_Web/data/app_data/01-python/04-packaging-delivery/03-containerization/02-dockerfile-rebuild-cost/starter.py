def rebuild_cost(dockerfile: list[dict], changed: set[str]) -> int:
    """
    `dockerfile` is a list of steps, in order. Each step is a dict:
      {"cmd": "FROM" | "COPY" | "ADD" | "RUN", "files": [paths], "cost": int}
    ("files" is only meaningful for COPY and ADD; it may be empty.)
    `changed` is the set of file paths that changed since the last build.

    A COPY or ADD step is invalidated if any of its files is in
    `changed`. Other steps are never invalidated directly. Once a step is
    invalidated, it and every step after it must be re-run.

    Return the total cost of the steps that must be re-run (0 if the
    cache is fully reused).
    """
    # TODO: implement this, see the Theory tab for the rules.
    pass
