---
name: math-kl-divergence
title: KL divergence between two distributions
tags: [information-theory]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`02-cross-entropy`'s Gibbs' inequality guarantees `H(p, q) >= H(p)`, cross-entropy is never smaller than the true distribution's own entropy. But it left one question unanswered: exactly HOW MUCH bigger is it? That gap, cross-entropy minus true entropy, is a distribution's own unavoidable baseline surprise subtracted out, isolates exactly the extra cost caused by `q` being a wrong (or imperfect) approximation of `p`. That gap is KL divergence, and unlike cross-entropy, it's zero precisely when the approximation is perfect, making it a genuine (if asymmetric) measure of "distance" between two distributions.

This measures the exact quantity model distillation minimizes (how far is a smaller "student" model's predicted distribution from a larger "teacher" model's), and it's the quantity variational inference and diffusion models are built on, both outside this curriculum's main path, but both direct extensions of the exact formula this question implements.

### From theory to code

Theory defines KL divergence as literally `cross_entropy(p, q) - entropy(p)`, the gap Gibbs' inequality guarantees is non-negative. Implement it as that one-line combination of the two functions you've already built.

Implement `kl_divergence(p, q, base=2.0)` against that reasoning. The signature and docstring are already in the editor.

### Constraints

- `kl_divergence(p, p, base)` must equal `0.0` (up to floating-point tolerance) for any valid distribution `p`.
- `kl_divergence` must never be negative.
- Reuse `entropy` and `cross_entropy` directly (both already imported at the top of the file), don't reimplement either formula.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

This is a one-line function: `cross_entropy(p, q, base) - entropy(p, base)`.

</details>

<details>
<summary>Hint 2</summary>

If your result isn't exactly `0.0` when `p == q`, double check you passed the SAME `base` to both `cross_entropy` and `entropy`.

</details>

## Theory

### The simple version

Imagine you built a weather forecast model for one city and are now using it, unmodified, to forecast weather in a very different city. Your forecast still produces SOME probability estimates, but how much worse is it, specifically, than a forecast built for the correct city? That "how much worse, specifically" is what KL divergence isolates: not the total surprise (that includes the weather's own inherent unpredictability, which no model could ever remove), just the EXTRA surprise caused by using the wrong model.

### The formula

```text
KL(p || q) = H(p, q) - H(p)
```

where `H(p, q)` is `02-cross-entropy`'s cross-entropy and `H(p)` is `01-entropy`'s entropy. Because Gibbs' inequality guarantees `H(p, q) >= H(p)` always, `KL(p || q) >= 0` always, with equality exactly when `q == p` (a perfect approximation costs zero extra bits).

Two properties worth knowing, both visible directly from this formula:

- **KL divergence is asymmetric**: `KL(p || q) != KL(q || p)` in general (subtracting `entropy(p)` vs `entropy(q)` are genuinely different quantities), which is why it's called a "divergence," not a "distance", a true distance would need to be symmetric.
- **KL divergence is zero exactly at a perfect match**, unlike cross-entropy, which is never zero (it's bounded below by `entropy(p)`, the distribution's own irreducible uncertainty). This makes KL the more natural quantity when you want "how far apart are these two distributions" rather than "how many total bits does this cost."

### How PyTorch actually implements this

`torch.nn.functional.kl_div` computes exactly this quantity (note: PyTorch's own convention takes `log(q)` as input rather than `q` directly, for the same log-space numerical-stability reasons `02-cross-entropy`'s `log_softmax` works in log-space). Knowledge distillation, training a smaller "student" network to mimic a larger "teacher" network's output distribution, minimizes exactly `KL(teacher_probs || student_probs)`, and variational autoencoders (VAEs) include a KL term in their loss that pulls a learned latent distribution toward a simple prior (usually a standard Normal), both are direct, practical uses of the exact formula implemented here, not abstract theory.

## Explanation

`kl_divergence` calls `cross_entropy(p, q, base)` and `entropy(p, base)` (both imported at the top of the file, already implemented in the preceding two questions) and returns their difference, exactly the formula from Theory, one line, reusing both prior questions rather than duplicating either formula.
