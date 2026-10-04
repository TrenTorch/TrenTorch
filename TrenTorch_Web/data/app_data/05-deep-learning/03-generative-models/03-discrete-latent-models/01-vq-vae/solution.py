import numpy as np


def vq_vae_loss(x_recon, x_true, z_e, z_q, beta=0.25):
    """Compute VQ-VAE loss.

    Args:
        x_recon: Reconstructed output, shape (N, D).
        x_true: True input, shape (N, D).
        z_e: Encoder latent, shape (N, D).
        z_q: Quantized latent, shape (N, D).
        beta: Commitment loss weight.

    Returns:
        Scalar loss.
    """
    recon_loss = np.mean((x_recon - x_true) ** 2)
    codebook_loss = np.mean((z_e.copy() - z_q) ** 2)
    commitment_loss = beta * np.mean((z_e - z_q.copy()) ** 2)
    return recon_loss + codebook_loss + commitment_loss
