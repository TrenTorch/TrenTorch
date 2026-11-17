---
name: vision-classifier-free-guidance
title: Classifier-Free Guidance
tags: [diffusion, generative-models, conditioning]
difficulty: Advanced
---

## Statement

### The problem, from first principles

A text-to-image model should follow its prompt, but a plainly conditioned diffusion model often produces images that only loosely match it. **Classifier-free guidance** sharpens the effect of the condition with no extra classifier. During training the condition (say, the text prompt) is randomly replaced by a special **null** condition some fraction of the time, so one network learns both the conditional and the unconditional noise prediction. At sampling time you evaluate the network twice at each step, with the prompt and without it, and **extrapolate** from the unconditional prediction past the conditional one: `eps = eps_uncond + w * (eps_cond - eps_uncond)`. A guidance scale `w = 1` is the plain conditional model and larger `w` trades diversity for prompt adherence.

### From theory to code

Implement `cfg_combine` and `drop_condition`.

### Constraints

- `cfg_combine(eps_uncond, eps_cond, w)` returns `eps_uncond + w * (eps_cond - eps_uncond)`.
- `drop_condition(cond_ids, p, null_id, rng)` returns a copy of the integer array `cond_ids` in which each entry is replaced by `null_id` with probability `p`. Draw exactly one array `u = rng.random_sample(len(cond_ids))` and replace entries where `u < p`. `rng` is a `np.random.RandomState`.
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

`w = 0` gives the unconditional prediction, `w = 1` the conditional one, and `w > 1` over-emphasizes the condition.

</details>

<details>
<summary>Hint 2</summary>

Drawing a single array keeps the training-time dropout reproducible from a seed.

</details>

## Theory

### The simple version

Compare what a painter would draw with and without your instructions. The _difference_ is what your instructions contribute. Guidance exaggerates that difference by a factor `w` to make the result follow instructions more strongly.

### The formula

$$
\tilde\epsilon = \epsilon_\theta(x_t, \varnothing) + w\,\big(\epsilon_\theta(x_t, c) - \epsilon_\theta(x_t, \varnothing)\big) = (1 - w)\,\epsilon_\theta(x_t, \varnothing) + w\,\epsilon_\theta(x_t, c)
$$

### How this is done in practice

Ho and Salimans introduced classifier-free guidance. Stable Diffusion typically uses `w` around 7.5, trains with about 10% condition dropout, and runs the conditional and unconditional passes as one batch of two. Very large `w` produces saturated, over-sharpened images.

## Explanation

The combine step is a linear extrapolation, and the dropout is a masked replacement driven by one random array. The tests check the three special values of `w` and the empirical drop rate.
