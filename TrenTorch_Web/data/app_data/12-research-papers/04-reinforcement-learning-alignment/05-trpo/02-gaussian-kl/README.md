---
name: research-trpo-gaussian-kl
title: 'TRPO: The KL Divergence Between Gaussians'
tags: [research-papers, reinforcement-learning, policy-gradient, trust-region]
difficulty: Advanced
---

## Statement

### The problem, from first principles

TRPO bounds how far the policy moves using a KL divergence between the old and new action distributions. For Gaussian policies, which continuous control uses, that divergence has a closed form in the means and standard deviations.

### From theory to code

Implement `gaussian_kl(mu1, s1, mu2, s2)` for the KL from the first Gaussian to the second.

### Constraints

- Standard deviations are positive.

### Hints

<details>
<summary>Hint 1</summary>

Use `log(s2/s1) + (s1^2 + (mu1 - mu2)^2) / (2 s2^2) - 1/2`.

</details>

## Theory

### The simple version

The divergence is zero only when both distributions match, grows with the mean shift, and penalizes changes in spread. TRPO caps this quantity to keep each update inside the trust region.

### The formula

$$D_{\text{KL}}\big(\mathcal{N}(\mu_1,\sigma_1^2)\,\|\,\mathcal{N}(\mu_2,\sigma_2^2)\big) = \log\frac{\sigma_2}{\sigma_1} + \frac{\sigma_1^2 + (\mu_1-\mu_2)^2}{2\sigma_2^2} - \frac{1}{2}$$

### How NumPy/PyTorch actually implements this

`torch.distributions.kl_divergence(Normal(mu1, s1), Normal(mu2, s2))` returns the same value.

## Explanation

The KL is asymmetric, which matters for which policy is treated as the reference in the trust region.
