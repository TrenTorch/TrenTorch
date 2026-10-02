import hashlib


def store_put(store: dict[str, bytes], data: bytes) -> str:
    """
    Save `data` in `store` (a dict mapping digest -> bytes) under its
    SHA-256 hex digest and return that digest. If the digest is already
    present, leave the store unchanged.
    """
    # TODO: implement this, see the Theory tab for the rules.
    pass


def dedupe_stats(blobs: list[bytes]) -> dict:
    """
    Put every blob into a fresh store with `store_put`, then return
      {"total_bytes": sum of the lengths of all blobs given,
       "stored_bytes": sum of the lengths of the blobs actually stored,
       "unique": the number of distinct blobs stored}
    """
    # TODO: implement this, see the Theory tab for the rules.
    pass
