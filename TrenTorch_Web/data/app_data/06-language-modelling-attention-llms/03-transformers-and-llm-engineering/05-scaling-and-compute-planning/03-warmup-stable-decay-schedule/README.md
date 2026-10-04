---
name: lm-warmup-stable-decay-schedule
title: Warmup-Stable-Decay Schedule
tags: [training, learning-rate, schedules]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

The cosine schedule needs to know the total number of training steps in advance, because it decays all the way to the end. That is inconvenient when you want to continue training, add data or branch off a checkpoint. The **warmup-stable-decay** (WSD) schedule has three phases. The learning rate warms up linearly to its peak, stays flat for most of the run, and is decayed only in a short final stretch. Any checkpoint taken during the stable phase can be turned into a finished model by running a decay phase from it, and the plateau avoids committing to a total length in advance.

### From theory to code

Implement `wsd_lr`.

### Constraints

- `wsd_lr(step, peak_lr, warmup_steps, decay_start, total_steps, final_ratio)` with `0 <= warmup_steps <= decay_start <= total_steps`.
- For `step < warmup_steps` the rate is `peak_lr * (step + 1) / warmup_steps`.
- For `warmup_steps <= step < decay_start` the rate is `peak_lr`.
- For `step >= decay_start` the rate falls linearly from `peak_lr` to `peak_lr * final_ratio`: with `p = (step - decay_start) / (total_steps - decay_start)` clipped to `[0, 1]` the rate is `peak_lr * (1 - p * (1 - final_ratio))`. If `decay_start == total_steps` the decay phase never begins.

### Hints

<details>
<summary>Hint 1</summary>

Check the phases in order and return early.

</details>

<details>
<summary>Hint 2</summary>

Clip the decay progress so steps beyond `total_steps` stay at the final rate.

</details>

## Theory

### The simple version

A runner warms up, holds a steady pace for most of the race and slows down only near the end. You can stop at any time during the steady pace and finish the run with a cool-down lap.

### The formula

$$
\eta(t) = \begin{cases}
\eta_{\max}\,\frac{t+1}{T_w} & t < T_w \\
\eta_{\max} & T_w \le t < T_d \\
\eta_{\max}\big(1 - p\,(1 - r)\big),\; p = \frac{t - T_d}{T - T_d} & t \ge T_d
\end{cases}
$$

### How this is done in practice

MiniCPM and several recent open models use WSD, and PyTorch's `LambdaLR` expresses it as a function of the step. The flat phase makes it easy to run a family of experiments that share a trunk and differ only in the decay.

## Explanation

The three branches map directly onto the three phases. The clip on the decay progress makes the function safe to call for steps beyond the planned total, which happens when a run is extended.
