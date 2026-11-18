
import numpy as np

from _load import load_solution

transformer_block_forward = load_solution("txf-block-assemble-full-block").transformer_block_forward


def vit_encoder_block(
    sequence: np.ndarray,
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
) -> np.ndarray:
    batched = sequence[None, :, :]
    output = transformer_block_forward(
        batched,
        num_heads,
        weight_o,
        bias_o,
        ffn_weight1,
        ffn_bias1,
        ffn_weight2,
        ffn_bias2,
        gamma1,
        beta1,
        gamma2,
        beta2,
    )
    return output[0]
