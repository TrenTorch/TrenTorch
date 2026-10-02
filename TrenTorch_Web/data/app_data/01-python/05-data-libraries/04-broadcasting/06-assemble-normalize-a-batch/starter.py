import numpy as np


def process_feature_batch(
    data: np.ndarray, feature_scales: np.ndarray, bias_per_sample: np.ndarray
) -> dict:
    """
    `data` is a 2D array of shape (num_samples, num_features).
    `feature_scales` is a 1D array of length num_features.
    `bias_per_sample` is a 1D array of length num_samples.

    Perform the following, in order:
      1. Scale every column of `data` by its corresponding value
         in `feature_scales`, using broadcasting. Call this
         `scaled`.
      2. Add `bias_per_sample[i]` to every element of row i of
         `scaled` — you will need to reshape `bias_per_sample`
         correctly using newaxis for this to broadcast in the
         intended direction. Call this `biased`.
      3. Attempt to add `feature_scales` directly to `biased`
         WITHOUT any reshaping, exactly as given. This may
         succeed or fail depending on the actual shapes involved
         — catch any resulting error rather than letting it
         propagate. Call the outcome `direct_add_attempt`.

    Return a dictionary:
      {
        "scaled": scaled,
        "biased": biased,
        "direct_add_success": <True if step 3 succeeded, False
            if it raised an error>,
        "direct_add_result": <the result if step 3 succeeded,
            else None>,
        "predicted_broadcast_shape": <the shape you would expect
            `biased` and `bias_per_sample` (correctly reshaped
            as in step 2) to broadcast to, computed directly
            rather than by trial>
      }
    """
    pass
