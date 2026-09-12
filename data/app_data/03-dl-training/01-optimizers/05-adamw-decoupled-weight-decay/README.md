---
name: dl-training-adamw-decoupled-weight-decay
title: 'AdamW: decoupled weight decay'
tags: [optimization]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`Ridge Regression (L2)` (Classical ML) added its penalty directly to the LOSS, `mse_loss + alpha * sum(weight^2)`. Differentiating that combined loss, the penalty shows up as an extra term ADDED INTO the gradient: `grad + 2*alpha*weight`. For plain SGD, adding that extra term to the gradient before the update is perfectly fine, mathematically identical to a direct parameter shrinkage. But `Adam: full update rule` doesn't just use the raw gradient, it feeds it through `m` and `v`, the adaptive moment estimates, BEFORE using it. Sneak a weight-decay term into the gradient before it enters that adaptive machinery, and it gets treated like any other gradient signal, divided by `sqrt(v_hat)` along with everything else, which means the ACTUAL amount of shrinkage a parameter receives ends up depending, unpredictably, on that parameter's own gradient history, not a clean, uniform "shrink every weight by this fixed fraction" the way L2 regularization is supposed to behave.

AdamW's fix has a name that says exactly what it does: DECOUPLE weight decay from the gradient-based update entirely. Apply it as its own, separate, always-the-same-size shrinkage step, directly to the parameter, with the adaptive Adam update layered on top, independently.

### From theory to code

Theory computes Adam's usual moment-based update (identical to `Adam: full update rule`), but applies weight decay as a SEPARATE term, `lr * weight_decay * param`, subtracted from the parameter directly, never mixed into the gradient or the moment estimates at all.

Implement `adamw_step(params, grads, m_list, v_list, t, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8, weight_decay=0.01)` against that reasoning.

### Constraints

- Weight decay applies to `param` DIRECTLY (`param - lr * weight_decay * param`), never added into `grad` before the moment updates.
- Everything else matches `Adam: full update rule`'s own structure exactly (reuse `update_moments` and `bias_correct`).
- `weight_decay` defaults to `0.01`, matching a common real-world default.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Compute the moment-based update exactly like `Adam: full update rule` does, unchanged.

</details>

<details>
<summary>Hint 2</summary>

Apply weight decay as a SEPARATE subtraction from `param` first (`param - lr * weight_decay * param`), THEN subtract the Adam update from that decayed value.

</details>

## Theory

### The simple version

A company wants every department's budget to shrink by a fixed 2% each quarter, regardless of how that department's spending has fluctuated recently. If instead that 2% shrinkage got mixed INTO each department's regular budget request before final approval, a department whose spending had been especially erratic (analogous to a large `v_hat`) would see that intended 2% cut get diluted or distorted by whatever adjustment process handles erratic requests. Keeping the 2% cut as its OWN separate, always-applied step, entirely apart from the regular budget adjustment process, is exactly what "decoupled" means, and exactly what AdamW does with weight decay.

### The formula

```text
m_new, v_new = update_moments(m, v, grad, beta1, beta2)   -- unchanged from Adam
m_hat = bias_correct(m_new, beta1, t)
v_hat = bias_correct(v_new, beta2, t)

decayed_param = param - lr * weight_decay * param          -- decoupled decay, applied FIRST
param_new     = decayed_param - lr * m_hat / (sqrt(v_hat) + eps)   -- then the usual Adam step
```

The gradient (`grad`) NEVER sees the weight decay term, it flows into `m` and `v` exactly as computed from the loss alone, so the ADAPTIVE part of Adam's update is entirely unaffected by decay. The decay itself is a plain, fixed fractional shrinkage (`lr * weight_decay`) applied uniformly to every parameter, entirely independent of that parameter's own gradient history, restoring the clean, predictable "shrink toward zero by a known amount" behavior `Ridge Regression (L2)`'s own L2 penalty was originally meant to provide.

### How PyTorch actually implements this

`torch.optim.AdamW` implements exactly this decoupled formula (this question's implementation matches it precisely, across multiple steps, verified directly against real PyTorch), and it has effectively become the DEFAULT optimizer choice for training modern transformer-based models (every large language model this curriculum's later Transformers/LLM content touches on is virtually always trained with AdamW, not plain Adam), specifically because this decoupling produces measurably better, more reliable regularization behavior at scale. The name itself, "AdamW," is literally "Adam" plus "(decoupled) Weight decay," a small, precise fix to a real, well-documented flaw in how the ORIGINAL Adam optimizer happened to interact with L2 regularization.

## Explanation

`adamw_step` computes `m_hat` and `v_hat` exactly like `Adam: full update rule`, unaffected by weight decay, then computes `decayed_param = param - lr * weight_decay * param` (the decoupled shrinkage, applied to the parameter directly), and finally subtracts the usual Adam moment-based update from THAT decayed value, exactly the two-part formula from Theory.
