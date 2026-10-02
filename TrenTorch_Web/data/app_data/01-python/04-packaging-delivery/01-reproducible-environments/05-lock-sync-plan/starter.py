def sync_plan(locked: dict[str, str], installed: dict[str, str], exact: bool = True) -> dict:
    """
    `locked` and `installed` both map package name -> exact version.

    Return {"install": [...], "remove": [...]} with sorted name lists:
      - "install": names in `locked` that are missing from `installed`
        or installed at a different version than locked
      - "remove": when `exact` is True, names in `installed` that are
        not in `locked`; when `exact` is False, always empty
    """
    # TODO: implement this, see the Theory tab for the rules.
    pass
