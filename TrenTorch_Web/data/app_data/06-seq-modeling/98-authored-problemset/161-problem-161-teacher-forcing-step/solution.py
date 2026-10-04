def solve(target, predicted, use_target):
    """Choose the ground-truth token or model prediction for the next step."""
    return target if use_target else predicted
