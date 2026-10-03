def _version_key(version: str) -> tuple:
    # TODO: implement this, see the Theory tab for the rules.
    pass


def stale_packages(declared: dict[str, str], locked: dict[str, str]) -> list[str]:
    """
    `declared` maps package name -> minimum allowed version ("2.0",
    "1.10.3", ...), meaning "version >= minimum".
    `locked` maps package name -> the one exact locked version.

    Return the sorted names of declared packages that the lock does NOT
    satisfy: the package is missing from `locked`, or its locked version
    is lower than the declared minimum.

    Versions are dotted integers compared numerically per component
    ("1.10" > "1.9"), and "1.2" equals "1.2.0".
    Packages in `locked` that are not declared (transitive dependencies)
    are ignored. Return [] when the lock is current.
    """
    # TODO: implement this, see the Theory tab for the rules.
    pass
