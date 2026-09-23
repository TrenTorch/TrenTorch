import hashlib


def compute_content_hash(data_bytes: bytes) -> str:
    """
    The actual fingerprint of a dataset's raw bytes: a SHA-256 hex
    digest. Same bytes in, same hash out, EVERY time -- that's the
    entire point of a cryptographic content hash.
    """
    # TODO: hashlib.sha256(data_bytes).hexdigest()
    pass


def hash_rows_naive(rows: list) -> str:
    """
    Hashes a dataset by converting its row list directly to bytes and
    hashing that -- this is "the same CSV" naively: if the rows are in
    a different ORDER, this produces a DIFFERENT hash, even though the
    underlying data is logically identical.
    """
    # TODO: compute_content_hash(repr(rows).encode())
    pass


def hash_rows_canonical(rows: list) -> str:
    """
    Fixes the naive version's row-order sensitivity: SORT the rows
    into one canonical order before hashing, so two datasets with the
    exact same rows (in any order) always produce the SAME hash.
    """
    # TODO: canonical = sorted(rows). Return
    # compute_content_hash(repr(canonical).encode()).
    pass


def datasets_are_identical(hash_a: str, hash_b: str) -> bool:
    """
    Two datasets are considered identical exactly when their hashes
    match -- the entire justification for using a hash as a dataset's
    "version" instead of, say, its filename or a human-written note.
    """
    # TODO: hash_a == hash_b
    pass
