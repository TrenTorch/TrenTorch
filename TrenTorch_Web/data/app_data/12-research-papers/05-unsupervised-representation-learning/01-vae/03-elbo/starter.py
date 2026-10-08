def elbo(log_px_given_z, kl):
    """
    log_px_given_z: reconstruction log-likelihood of the data given a sampled latent
    kl: KL divergence between the approximate posterior and the prior

    Returns:
        The evidence lower bound log_px_given_z - kl, to be maximized.
    """
    # TODO: Subtract the KL from the reconstruction term (see Theory).
    pass
