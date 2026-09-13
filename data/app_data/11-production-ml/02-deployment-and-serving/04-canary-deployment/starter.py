import hashlib


def hash_bucket(key: str, num_buckets: int = 100) -> int:
    """
    A deterministic, uniformly-spread bucket number (0 to
    num_buckets-1) for a given key, derived from a real cryptographic
    hash -- the SAME key always lands in the SAME bucket, and across
    many different keys, buckets are hit roughly evenly.
    """
    # TODO: digest = hashlib.sha256(key.encode()).hexdigest(). Return
    # int(digest, 16) % num_buckets.
    pass


def is_routed_to_canary(request_id: str, canary_percentage: float) -> bool:
    """
    Deterministically decides whether a given request_id routes to the
    canary: using hash_bucket with 100 buckets, a request routes to
    the canary exactly when its bucket falls below canary_percentage
    -- so canary_percentage=10 sends roughly 10% of ALL possible
    request_ids to the canary, consistently (the SAME request_id is
    ALWAYS routed the same way, unlike a coin-flip per request).
    """
    # TODO: hash_bucket(request_id, num_buckets=100) < canary_percentage
    pass


def route_request(request_id: str, canary_percentage: float, canary_model_fn, stable_model_fn):
    """
    Actually dispatches a request to whichever model
    is_routed_to_canary says it belongs to.
    """
    # TODO: if is_routed_to_canary(...), call canary_model_fn(request_id);
    # otherwise call stable_model_fn(request_id).
    pass
