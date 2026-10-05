import hashlib


def build_manifest(files: dict[str, bytes]) -> dict:
    """
    `files` maps a relative path to that file's bytes.

    Return a dict with:
      "entries": a list of {"path": path, "sha256": hex digest of the
                 file's bytes}, sorted by path
      "nfiles":  the number of files
      "size":    the total number of bytes across all files
      "digest":  the SHA-256 hex digest of this exact text, encoded as
                 UTF-8: one line "<path>\t<sha256>" per entry, in sorted
                 order, joined with "\n" (no trailing newline).
                 An empty directory hashes the empty string.
    """
    # TODO: implement this, see the Theory tab for the rules.
    pass
