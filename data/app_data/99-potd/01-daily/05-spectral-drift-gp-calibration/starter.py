import numpy as np

R_H = 1.097373e7  # m^-1, fixed by the problem -- do not substitute a different value


def rydberg_wavelength_nm(n1: int, n2: int) -> float:
    """
    Theoretical vacuum wavelength (nanometers) of the photon emitted by an
    electron transition n2 -> n1, via the Rydberg formula:

        1/lambda = R_H * (1/n1^2 - 1/n2^2)      (lambda in meters)

    Use exactly R_H = 1.097373e7 m^-1 (defined above). Convert to
    nanometers (1 m = 1e9 nm) before returning.
    """
    pass


def gp_calibrate(
    training: list[tuple[int, int, float]],
    sigma_f: float,
    l: float,
    sigma_n: float,
    queries: list[tuple[int, int]],
) -> np.ndarray:
    """
    Exact Gaussian Process regression over the spectrometer's calibration
    drift, solved via Cholesky decomposition (no explicit matrix inverse).

    training: list of (n1, n2, measured_wavelength_nm) tuples.
    sigma_f, l, sigma_n: RBF kernel signal std, length scale (nm), and
        observation noise std (all > 0).
    queries: list of (n1, n2) transitions to predict.

    Steps:
      1. For each training row, compute the theoretical wavelength x_i via
         rydberg_wavelength_nm, and the calibration residual
         y_i = measured_i - x_i. This (x_i, y_i) pair is what the GP is
         trained on.
      2. Build the n x n kernel matrix K with
         K_ij = sigma_f^2 * exp(-(x_i - x_j)^2 / (2 * l^2)).
      3. Cholesky-factor A = K + sigma_n^2 * I as A = L @ L.T, then solve
         L @ z = y and L.T @ alpha = z (two triangular solves, not a
         matrix inverse) to get alpha.
      4. For each query (q_n1, q_n2): compute x_star via
         rydberg_wavelength_nm, k_star = [k(x_i, x_star)]_i, then:
             mu(x_star)     = k_star @ alpha
             v              = solve L @ v = k_star  (forward substitution)
             sigma^2(x_star) = sigma_f^2 - v @ v
         Output row is (x_star + mu(x_star), sqrt(sigma^2(x_star))).

    Returns an (m, 2) array: column 0 is the predicted (calibration-
    corrected) wavelength in nm, column 1 is the posterior uncertainty
    (std dev, nm), in the same order as `queries`.
    """
    pass
