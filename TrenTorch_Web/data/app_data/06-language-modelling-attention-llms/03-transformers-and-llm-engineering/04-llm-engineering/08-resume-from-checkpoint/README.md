---
name: txf-llmeng-resume-from-checkpoint
title: 'Resume-from-checkpoint: restoring optimizer state, not just weights'
tags: [transformers, nlp]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Large-scale LLM training runs for days or weeks, and interruptions (hardware failures, scheduled maintenance, deliberately pausing to change something) are a genuine, routine part of the process, not a rare edge case. Resuming correctly means far more than just reloading the model's WEIGHTS: `[03-dl-training/01-optimizers/04-adam-full-update]`'s Adam optimizer maintains its OWN persistent per-parameter state across steps, the running first-moment estimate `m` and second-moment estimate `v`, PLUS a step counter `t` used for bias correction. If a checkpoint saves only the weights and discards this optimizer state, resuming training effectively means restarting Adam's internal history from scratch, with `m`/`v` reset to zero and `t` reset to `1`, even though the WEIGHTS themselves are already well into training. This produces a measurably DIFFERENT training trajectory than an uninterrupted run would have taken, exactly the kind of subtle bug that's easy to introduce (checkpointing code that "just" saves `model.state_dict()` and forgets `optimizer.state_dict()`) and easy to miss in short experiments, since the damage only compounds over many resumed steps.

### From theory to code

Implement `save_checkpoint(params, m_list, v_list, t)` (saving everything needed to resume identically), `train_n_steps` (running `[04-adam-full-update]`'s `adam_step` repeatedly), `resume_from_full_checkpoint` (the CORRECT way), and `resume_from_weights_only` (the WRONG way, included specifically to demonstrate the difference).

### Constraints

- `save_checkpoint` copies (never merely references) `params`, `m_list`, and `v_list`, so later in-place mutation of the originals cannot silently corrupt an already-saved checkpoint.
- `resume_from_full_checkpoint` continues training using the checkpoint's OWN `m_list`, `v_list`, and `t`, exactly where they left off.
- `resume_from_weights_only` reinitializes `m_list`/`v_list` to zero-filled arrays and `t` to `1`, discarding all prior optimizer history, deliberately reproducing the buggy behavior this question is built to expose.
- Given the SAME sequence of gradients, `resume_from_full_checkpoint` must reproduce an uninterrupted run's final weights EXACTLY (up to floating-point precision); `resume_from_weights_only` must NOT.

### Hints

<details>
<summary>Hint 1: Saving a full checkpoint</summary>

```python
return dict(
    params=[p.copy() for p in params],
    m_list=[m.copy() for m in m_list],
    v_list=[v.copy() for v in v_list],
    t=t,
)
```

</details>

<details>
<summary>Hint 2: The two resume paths</summary>

```python
def resume_from_full_checkpoint(checkpoint, grads_sequence, lr):
    return train_n_steps(checkpoint["params"], checkpoint["m_list"], checkpoint["v_list"], checkpoint["t"], grads_sequence, lr)

def resume_from_weights_only(params, grads_sequence, lr):
    m_list = [np.zeros_like(p) for p in params]
    v_list = [np.zeros_like(p) for p in params]
    return train_n_steps(params, m_list, v_list, 1, grads_sequence, lr)   # t reset to 1!
```

</details>

## Theory

### The simple version

A runner training for a marathon who tracks not just their current fitness level (the WEIGHTS) but also their recent pace history, how their body has been adapting week over week (Adam's `m`/`v`, a kind of running "momentum" and "adaptive step size" memory). If an injury forces a break, resuming training by only remembering their fitness level, but forgetting their entire recent pace history and treating week one of the comeback as if it were literally their very first week of training ever, produces a genuinely different, generally WORSE training trajectory than if their coach had kept full notes and picked up exactly where they left off.

### The formula

```
Correct:   resume with (params, m, v, t) all restored from the checkpoint
Incorrect: resume with (params) restored, but (m=0, v=0, t=1) reset to fresh-start values
```

Both paths apply the IDENTICAL `adam_step` update rule at every subsequent step; only the STARTING state going into that rule differs, and Adam's update explicitly depends on `m`, `v`, and `t` (via bias correction), so different starting state means a genuinely different resulting update at every subsequent step.

### How PyTorch actually implements this

`torch.save({'model': model.state_dict(), 'optimizer': optimizer.state_dict()}, path)` is the standard, correct PyTorch checkpointing pattern: `optimizer.state_dict()` includes exactly Adam's per-parameter `exp_avg` (`m`), `exp_avg_sq` (`v`), and `step` (`t`) for every parameter, alongside the hyperparameters. A checkpointing bug that saves only `model.state_dict()` (a genuinely common real mistake, since the model's weights are the more obviously important-seeming artifact) reproduces exactly this question's `resume_from_weights_only` failure mode, silently degrading training after every resume without necessarily causing an outright crash, which is precisely what makes it a dangerous, easy-to-miss bug in practice.

## Explanation

`save_checkpoint` copies every piece of state a resumed training run genuinely needs: not just `params`, but Adam's own `m_list`/`v_list` moving averages and the step counter `t` its bias correction depends on. `train_n_steps` threads all four pieces of state through `[04-adam-full-update]`'s `adam_step`, once per entry in `grads_sequence`. `resume_from_full_checkpoint` hands the checkpoint's saved `m_list`, `v_list`, and `t` straight into `train_n_steps`, continuing the optimizer's internal history exactly where it left off, which is precisely why it reproduces an uninterrupted run's results bit-for-bit. `resume_from_weights_only` instead reinitializes `m_list`/`v_list` to zero and `t` to `1`, exactly as if training had never happened before this point, and because Adam's update genuinely depends on that history (bias-corrected moving averages, not a stateless computation), this produces a measurably different sequence of updates from that point forward, the concrete, demonstrable cost of a checkpoint that saves weights without also saving optimizer state.
