import numpy as np

def solve(context_limit,prompt_tokens):
        return max(0,context_limit-prompt_tokens)
