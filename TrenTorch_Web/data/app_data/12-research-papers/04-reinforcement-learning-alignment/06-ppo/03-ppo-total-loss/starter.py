def ppo_total_loss(clip_obj, vf_loss, entropy, c1, c2):
    """
    clip_obj: the clipped policy objective to maximize
    vf_loss: squared error of the value function
    entropy: mean policy entropy (encourages exploration)
    c1: weight on the value loss
    c2: weight on the entropy bonus

    Returns:
        The loss to minimize: -(clip_obj - c1 * vf_loss + c2 * entropy).
    """
    # TODO: Combine the three terms with their weights and negate them for minimization (see Theory).
    pass
