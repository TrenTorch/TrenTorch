def solve(x, norm, attention, ff):
    """Apply a pre-norm transformer block with attention and feed-forward residuals."""
    first = x + attention(norm(x))
    return first + ff(norm(first))
