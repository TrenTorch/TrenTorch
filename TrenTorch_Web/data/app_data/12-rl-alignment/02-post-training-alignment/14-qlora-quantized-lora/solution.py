import numpy as np


def compute_int8_scale(weight: np.ndarray) -> float:
    return float(np.max(np.abs(weight)) / 127.0)


def quantize_int8(weight: np.ndarray, scale: float) -> np.ndarray:
    return np.clip(np.round(weight / scale), -128, 127).astype(np.int8)


def dequantize_int8(quantized_weight: np.ndarray, scale: float) -> np.ndarray:
    return quantized_weight.astype(np.float32) * scale


def lora_delta(input: np.ndarray, lora_A: np.ndarray, lora_B: np.ndarray, alpha: float, rank: int) -> np.ndarray:
    return (alpha / rank) * (input @ lora_A.T) @ lora_B.T


def qlora_linear_forward(
    input: np.ndarray, quantized_weight: np.ndarray, scale: float, lora_A: np.ndarray, lora_B: np.ndarray, alpha: float, rank: int
) -> np.ndarray:
    base_weight = dequantize_int8(quantized_weight, scale)
    base_output = input @ base_weight.T
    return base_output + lora_delta(input, lora_A, lora_B, alpha, rank)


def count_trainable_parameters(in_features: int, out_features: int, rank: int) -> dict:
    full_finetune_params = in_features * out_features
    qlora_params = rank * in_features + out_features * rank
    return {"full_finetune": full_finetune_params, "qlora": qlora_params}
