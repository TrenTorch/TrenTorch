def ppo_total_loss(clip_obj, vf_loss, entropy, c1, c2):
    return -(clip_obj - c1 * vf_loss + c2 * entropy)
