import hashlib


def store_put(store: dict[str, bytes], data: bytes) -> str:
    """
    Save `data` in `store` (a dict mapping digest -> bytes) under its
    SHA-256 hex digest and return that digest. If the digest is already
    present, leave the store unchanged.
    """
    digest = hashlib.sha256(data).hexdigest()
    store.setdefault(digest, data)
    return digest


def dedupe_stats(blobs: list[bytes]) -> dict:
    """
    Put every blob into a fresh store with `store_put`, then return
      {"total_bytes": sum of the lengths of all blobs given,
       "stored_bytes": sum of the lengths of the blobs actually stored,
       "unique": the number of distinct blobs stored}
    """
    store: dict[str, bytes] = {}
    for blob in blobs:
        store_put(store, blob)
    return {
        "total_bytes": sum(len(blob) for blob in blobs),
        "stored_bytes": sum(len(blob) for blob in store.values()),
        "unique": len(store),
    }
