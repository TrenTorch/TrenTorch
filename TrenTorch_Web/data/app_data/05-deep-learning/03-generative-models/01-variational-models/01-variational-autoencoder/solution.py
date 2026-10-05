import numpy as np


def vae_loss(x_recon, x_true, mu, logvar):
    """Compute VAE loss (ELBO).

    Args:
        x_recon: Reconstructed output, shape (N, D).
        x_true: True input, shape (N, D).
        mu: Latent mean, shape (N, latent_dim).
        logvar: Latent log-variance, shape (N, latent_dim).

    Returns:
        Scalar loss (ELBO).
    """
    recon_loss = np.mean((x_recon - x_true) ** 2)
    kl_loss = -0.5 * np.mean(1 + logvar - mu ** 2 - np.exp(logvar))
    return recon_loss + kl_loss
