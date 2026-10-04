import numpy as np

def solve(backbone, head, base_lr, backbone_factor):
    """Implement fine-tuning lr groups according to the contract."""
    return [{'params': backbone, 'lr': base_lr * backbone_factor}, {'params': head, 'lr': base_lr}]
