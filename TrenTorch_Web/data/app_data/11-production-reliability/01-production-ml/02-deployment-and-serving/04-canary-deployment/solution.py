import hashlib


def hash_bucket(key: str, num_buckets: int = 100) -> int:
    digest = hashlib.sha256(key.encode()).hexdigest()
    return int(digest, 16) % num_buckets


def is_routed_to_canary(request_id: str, canary_percentage: float) -> bool:
    return hash_bucket(request_id) < canary_percentage


def route_request(request_id: str, canary_percentage: float, canary_model_fn, stable_model_fn):
    if is_routed_to_canary(request_id, canary_percentage):
        return canary_model_fn(request_id)
    return stable_model_fn(request_id)
