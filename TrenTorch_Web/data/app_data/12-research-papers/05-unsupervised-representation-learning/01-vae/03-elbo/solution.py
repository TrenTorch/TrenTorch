def elbo(log_px_given_z, kl):
    return log_px_given_z - kl
