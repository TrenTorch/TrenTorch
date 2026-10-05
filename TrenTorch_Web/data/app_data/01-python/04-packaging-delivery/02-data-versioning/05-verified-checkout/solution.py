import hashlib


def checkout(manifest: dict[str, str], store: dict[str, bytes]) -> dict[str, bytes]:
    """
    `manifest` maps a path to a SHA-256 hex digest.
    `store` maps a SHA-256 hex digest to bytes.

    Return a dict mapping each manifest path to its bytes.
    Go through the manifest in sorted path order and, for each entry:
      - if the digest is not in `store`, raise FileNotFoundError
      - if the stored bytes do not hash (SHA-256) to that digest, raise
        ValueError
    Return nothing partial: either every file is returned or an error is
    raised. An empty manifest returns {}.
    """
    files = {}
    for path in sorted(manifest):
        digest = manifest[path]
        if digest not in store:
            raise FileNotFoundError(f"missing blob {digest} for {path}")
        data = store[digest]
        if hashlib.sha256(data).hexdigest() != digest:
            raise ValueError(f"corrupt blob {digest} for {path}")
        files[path] = data
    return files
