import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

feedforward_sublayer = load_solution("05-transformers-llm/01-transformer-block/04-feedforward-sublayer").feedforward_sublayer
softmax_last_axis = load_solution("04-seq-modeling/04-attention/03-softmax-last-axis").softmax_last_axis


def moe_gate(x: np.ndarray, gate_weight: np.ndarray, top_k: int) -> tuple[np.ndarray, np.ndarray]:
    """
    Top-k gating: scores every expert via `x @ gate_weight.T` (shape
    `(..., num_experts)`), keeps only the `top_k` HIGHEST-scoring experts
    per token, and re-normalizes just those `top_k` scores with softmax
    (so the selected experts' weights still sum to `1`, even though most
    experts were discarded entirely). Returns `(top_indices, top_weights)`,
    both shape `(..., top_k)`.
    """
    pass


def moe_ffn_forward(
    x: np.ndarray,
    gate_weight: np.ndarray,
    expert_params: list[dict],
    top_k: int,
) -> np.ndarray:
    """
    Routes every token to its own top-`k` experts (via `moe_gate`), runs
    EACH selected expert's own `[01-transformer-block/04-feedforward-sublayer]`-style
    FFN on that token, and combines the `top_k` experts' outputs via a
    WEIGHTED SUM using the gate weights. `expert_params` is a list of
    dicts, one per expert, each with `weight1`/`bias1`/`weight2`/`bias2`.
    """
    pass
