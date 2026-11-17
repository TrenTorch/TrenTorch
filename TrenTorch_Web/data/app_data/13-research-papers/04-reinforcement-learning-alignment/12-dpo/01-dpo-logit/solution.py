def dpo_logit(logp_w, logp_l, ref_w, ref_l, beta):
    return beta * ((logp_w - ref_w) - (logp_l - ref_l))
