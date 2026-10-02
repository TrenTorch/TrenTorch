import numpy as np


def _broadcast_result_shape(shape_a: tuple, shape_b: tuple) -> tuple:
    length = max(len(shape_a), len(shape_b))
    padded_a = (1,) * (length - len(shape_a)) + tuple(shape_a)
    padded_b = (1,) * (length - len(shape_b)) + tuple(shape_b)
    return tuple(max(a, b) for a, b in zip(padded_a, padded_b))


def process_feature_batch(
    data: np.ndarray, feature_scales: np.ndarray, bias_per_sample: np.ndarray
) -> dict:
    scaled = data * feature_scales
    reshaped_bias = bias_per_sample[:, np.newaxis]
    biased = scaled + reshaped_bias

    try:
        direct_add_result = biased + feature_scales
        direct_add_success = True
    except ValueError:
        direct_add_result = None
        direct_add_success = False

    predicted_broadcast_shape = _broadcast_result_shape(biased.shape, reshaped_bias.shape)

    return {
        "scaled": scaled,
        "biased": biased,
        "direct_add_success": direct_add_success,
        "direct_add_result": direct_add_result,
        "predicted_broadcast_shape": predicted_broadcast_shape,
    }
