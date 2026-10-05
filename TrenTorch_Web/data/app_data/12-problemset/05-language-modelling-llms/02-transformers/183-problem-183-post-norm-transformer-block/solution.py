import numpy as np

def solve(x, norm, attention, ff):
    """Apply attention and feed-forward residuals, normalizing after each residual."""
    x = np.asarray(x)
    attention_output = np.asarray(attention(x))
    after_attention = norm(x + attention_output)
    feed_forward_output = np.asarray(ff(after_attention))
    return norm(after_attention + feed_forward_output)
