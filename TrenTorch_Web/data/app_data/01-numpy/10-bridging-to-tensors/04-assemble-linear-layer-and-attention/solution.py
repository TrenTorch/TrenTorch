import numpy as np


def init_linear_params(
    rng: np.random.Generator, in_features: int, out_features: int, device: str = "cpu"
) -> dict:
    W_data = rng.normal(
        0.0, np.sqrt(2.0 / in_features), (in_features, out_features)
    ).astype(np.float32)
    b_data = np.zeros(out_features, dtype=np.float32)

    return {
        "W": {"data": W_data, "device": device, "requires_grad": True},
        "b": {"data": b_data, "device": device, "requires_grad": True},
    }


def linear_forward(x: dict, params: dict) -> dict:
    W = params["W"]
    b = params["b"]

    devices = {x["device"], W["device"], b["device"]}
    if len(devices) > 1:
        raise ValueError(f"devices differ: {devices}")

    if x["data"].shape[-1] != W["data"].shape[0]:
        raise ValueError(
            f"shape mismatch: x last dim {x['data'].shape[-1]} != W first dim {W['data'].shape[0]}"
        )

    data = x["data"] @ W["data"] + b["data"]
    requires_grad = x["requires_grad"] or W["requires_grad"] or b["requires_grad"]

    return {"data": data, "device": x["device"], "requires_grad": requires_grad}


def attention_weights(q: np.ndarray, k: np.ndarray) -> np.ndarray:
    if q.shape[-1] != k.shape[-1]:
        raise ValueError(f"last dims differ: {q.shape[-1]} != {k.shape[-1]}")

    d = q.shape[-1]
    scores = (q @ k.T) / np.sqrt(d)
    scores_stable = scores - scores.max(axis=1, keepdims=True)
    exp_scores = np.exp(scores_stable)
    return exp_scores / exp_scores.sum(axis=1, keepdims=True)
