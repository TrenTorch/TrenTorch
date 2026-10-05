
import numpy as np

from _load import load_solution

layer_norm_forward = load_solution("txf-block-layer-norm-forward").layer_norm_forward
residual_connection = load_solution("txf-block-residual-connection").residual_connection
feedforward_sublayer = load_solution("txf-block-feedforward-sublayer").feedforward_sublayer
multi_head_attention = load_solution("seq-attention-mha-concat-output-projection").multi_head_attention


def transformer_block_forward(
    x: np.ndarray,
    num_heads: int,
    weight_o: np.ndarray,
    bias_o: np.ndarray,
    ffn_weight1: np.ndarray,
    ffn_bias1: np.ndarray,
    ffn_weight2: np.ndarray,
    ffn_bias2: np.ndarray,
    gamma1: np.ndarray,
    beta1: np.ndarray,
    gamma2: np.ndarray,
    beta2: np.ndarray,
    mask: np.ndarray | None = None,
    eps: float = 1e-5,
) -> np.ndarray:
    """
    One full Pre-Norm Transformer block, assembled entirely from pieces
    already built earlier in this curriculum:

      x1 = x  + MultiHeadAttention(LayerNorm(x, gamma1, beta1))
      x2 = x1 + FeedForward(LayerNorm(x1, gamma2, beta2))
      return x2

    Self-attention: `query = key = value = LayerNorm(x, gamma1, beta1)`.
    """
    pass
