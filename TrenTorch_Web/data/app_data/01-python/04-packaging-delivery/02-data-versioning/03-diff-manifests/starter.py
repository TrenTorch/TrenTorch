def diff_manifests(old: dict[str, str], new: dict[str, str]) -> dict:
    """
    `old` and `new` map a file path to its content hash.

    Return {"added": [...], "removed": [...], "modified": [...]}, each a
    sorted list of paths:
      - added:    in `new` but not in `old`
      - removed:  in `old` but not in `new`
      - modified: in both, with different hashes
    Paths with identical hashes appear nowhere.
    """
    # TODO: implement this, see the Theory tab for the rules.
    pass
