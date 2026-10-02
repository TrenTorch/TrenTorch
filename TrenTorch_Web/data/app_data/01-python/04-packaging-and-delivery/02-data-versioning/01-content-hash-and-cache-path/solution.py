import hashlib


def content_hash(chunks) -> str:
    """
    `chunks` is any iterable of `bytes` objects (e.g. a generator reading
    a big file piece by piece). Return the SHA-256 hex digest of all the
    chunks joined together, without ever joining them into one bytes
    object. The result must not depend on how the data was split into
    chunks. An empty iterable hashes like empty data.
    """
    digest = hashlib.sha256()
    for chunk in chunks:
        digest.update(chunk)
    return digest.hexdigest()


def cache_path(digest: str) -> str:
    """
    Return the sharded cache location of a hex digest: the first two
    characters, a "/", then the remaining characters.
    cache_path("2cf24dba5f...") == "2c/f24dba5f..."
    """
    return f"{digest[:2]}/{digest[2:]}"
