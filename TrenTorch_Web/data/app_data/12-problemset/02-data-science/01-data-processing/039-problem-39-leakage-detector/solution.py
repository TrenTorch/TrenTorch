import numpy as np

def solve(columns):
    forbidden = ("target", "label", "future", "outcome", "post_")
    return [column for column in columns if any(term in column.lower() for term in forbidden)]
