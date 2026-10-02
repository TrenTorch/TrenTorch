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
    entries = [
        {"path": path, "sha256": hashlib.sha256(files[path]).hexdigest()}
        for path in sorted(files)
    ]
    text = "\n".join(f"{entry['path']}\t{entry['sha256']}" for entry in entries)
    return {
        "entries": entries,
        "nfiles": len(entries),
        "size": sum(len(data) for data in files.values()),
        "digest": hashlib.sha256(text.encode("utf-8")).hexdigest(),
    }
