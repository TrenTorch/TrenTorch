def solve(backbone, head):
    """Freeze backbone parameters and leave task-head parameters trainable."""
    for parameter in backbone:
        parameter.requires_grad = False
    for parameter in head:
        parameter.requires_grad = True
    return list(backbone), list(head)
