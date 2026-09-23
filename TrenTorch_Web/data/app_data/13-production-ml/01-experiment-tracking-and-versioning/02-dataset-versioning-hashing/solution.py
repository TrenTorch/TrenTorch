import hashlib


def compute_content_hash(data_bytes: bytes) -> str:
    return hashlib.sha256(data_bytes).hexdigest()


def hash_rows_naive(rows: list) -> str:
    return compute_content_hash(repr(rows).encode())


def hash_rows_canonical(rows: list) -> str:
    canonical = sorted(rows)
    return compute_content_hash(repr(canonical).encode())


def datasets_are_identical(hash_a: str, hash_b: str) -> bool:
    return hash_a == hash_b
