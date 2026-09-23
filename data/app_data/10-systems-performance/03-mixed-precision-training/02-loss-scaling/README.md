---
name: systems-perf-loss-scaling
title: 'Loss Scaling: Scale the Loss Before Backward, Unscale Gradients Before the Step'
tags: [mlops, neural-networks, mixed-precision]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`01-fp16-bf16-representable-range` showed that `float16` values smaller than roughly `6e-8` vanish to exactly `0.0` — and real gradients, especially late in training or in deep networks, routinely take on values in exactly that danger zone. If a gradient silently underflows to zero, its parameter simply stops updating, with no error raised anywhere.

### From theory to code

Implement `scale_loss(loss, scale)`, `unscale_gradients(gradients, scale)`, and `has_inf_or_nan(gradients)`. The trick: multiply the loss by some large `scale` _before_ backpropagation (every gradient scales up by the same factor, via the chain rule), keeping them safely away from the underflow floor throughout backward — then divide back down by `scale` _after_ backward, before the optimizer actually uses them.

### Constraints

- `scale_loss(loss, scale)` returns `loss * scale`.
- `unscale_gradients(gradients, scale)` returns each gradient array divided by `scale`, same shapes, as a new list.
- `has_inf_or_nan(gradients)` returns `True` if any element in any gradient array is `inf` or `nan`; `False` (including for an empty list) otherwise.
- None of the three mutate their inputs.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

The chain rule means scaling the loss by a constant scales every gradient computed from it by that exact same constant — so a gradient that would have been `1e-6` (dangerously close to fp16's floor) becomes `1e-6 * scale`, comfortably clear of it, if `scale` is large enough.

</details>

<details>
<summary>Hint 2</summary>

`np.isfinite(g)` is `False` for both `inf` and `nan` — checking `not np.all(np.isfinite(g))` per array, then combining across the whole list with `any(...)`, catches either failure mode in one pass.

</details>

## Theory

### The simple version

Think of loss scaling as temporarily talking louder specifically so a quiet voice doesn't get lost in the noise floor: multiply everything up before it has a chance to underflow, do all the fragile fp16 arithmetic at that safely-loud volume, then turn the volume back down by the exact same amount right before the result actually gets used — the content never changed, only how loud it had to be to survive the trip.

### The formula

```text
scaled_loss = loss * scale
grads       = backward(scaled_loss)          # every grad is now `scale` times too large
if has_inf_or_nan(grads):
    skip this step, reduce `scale`, try again
else:
    real_grads = grads / scale                # unscale_gradients
    optimizer.step(real_grads)
```

Real implementations don't pick one fixed `scale` and leave it forever — they use _dynamic_ loss scaling: start with a large `scale`, and if `has_inf_or_nan` ever fires (meaning `scale` pushed some gradient into fp16's _overflow_ ceiling instead of just avoiding its underflow floor), skip that step's update entirely and shrink `scale`; if many consecutive steps pass cleanly, grow `scale` back up to stay as far from the underflow floor as safely possible.

### How PyTorch actually implements this

`torch.cuda.amp.GradScaler` implements exactly this dynamic loss-scaling loop: `scaler.scale(loss).backward()` performs `scale_loss` and the backward pass together, `scaler.step(optimizer)` internally checks for inf/nan (skipping the step if found) and otherwise unscales before calling `optimizer.step()`, and `scaler.update()` adjusts `scale` up or down based on whether overflow was detected that step — the same three operations this exercise implements by hand, packaged into one stateful helper class.

## Explanation

`scale_loss` is `loss * scale` directly — the single multiplication that, via the chain rule, scales every gradient computed from it by the same factor.

`unscale_gradients` returns a new list, `[g / scale for g in gradients]`, dividing every gradient array back down to its true magnitude — building a new list (rather than modifying in place) keeps the caller's original scaled gradients untouched, matching this exercise's no-mutation constraint.

`has_inf_or_nan` checks `np.isfinite(g)` for every array `g` in `gradients` — `np.isfinite` is `False` for both `inf` and `nan` in one check, so `not np.all(np.isfinite(g))` catches either failure mode per array, and `any(...)` across the whole list means a single bad gradient anywhere is enough to flag the entire step as unsafe.
