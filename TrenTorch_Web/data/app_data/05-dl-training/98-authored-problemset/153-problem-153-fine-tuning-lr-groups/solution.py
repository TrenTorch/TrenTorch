def solve(backbone, head, base_lr, backbone_factor):
    """Build optimizer groups with a scaled backbone and base-rate head."""
    return [
        {"params": list(backbone), "lr": base_lr * backbone_factor},
        {"params": list(head), "lr": base_lr},
    ]
