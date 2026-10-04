import numpy as np

def solve(backbone, head):
    """Implement transfer learning freeze according to the contract."""
    for p in backbone:
        p.requires_grad = False
    for p in head:
        p.requires_grad = True
    return (list(backbone), list(head))
