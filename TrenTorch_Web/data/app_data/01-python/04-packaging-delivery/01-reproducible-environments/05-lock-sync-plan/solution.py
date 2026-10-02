def sync_plan(locked: dict[str, str], installed: dict[str, str], exact: bool = True) -> dict:
    """
    `locked` and `installed` both map package name -> exact version.

    Return {"install": [...], "remove": [...]} with sorted name lists:
      - "install": names in `locked` that are missing from `installed`
        or installed at a different version than locked
      - "remove": when `exact` is True, names in `installed` that are
        not in `locked`; when `exact` is False, always empty
    """
    install = sorted(name for name, version in locked.items() if installed.get(name) != version)
    remove = sorted(name for name in installed if name not in locked) if exact else []
    return {"install": install, "remove": remove}
