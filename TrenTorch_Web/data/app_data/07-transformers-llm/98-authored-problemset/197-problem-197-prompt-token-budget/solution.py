import numpy as np

def solve(context_limit, prompt_tokens):
    """Implement prompt token budget according to the contract."""
    return max(0, context_limit - prompt_tokens)
