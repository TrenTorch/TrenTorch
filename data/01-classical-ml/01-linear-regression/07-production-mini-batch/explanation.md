`rng.permutation(n_samples)` is regenerated fresh inside the epoch loop, not once outside it — a single reused permutation would train on the identical batch order every epoch, defeating the entire point of shuffling.

`batch_idx = order[start:start + batch_size]` slices the _shuffled index array_, not `X` directly, so `X` and `y` stay correctly paired to the same samples no matter how they're reordered.

The final, possibly-shorter batch needs no special-case: `range(0, n_samples, batch_size)`'s last `start` value naturally produces a shorter slice on its own — no `if` branch needed for the remainder.

Reusing `linear_forward` / `mse_grad` / `gd_step` unchanged — just called on `X_batch` instead of `X` — is the actual point of the exercise: production and naive training aren't different algorithms, they're the same three functions called at a different granularity.

`rng = np.random.default_rng(seed)` sits _outside_ the epoch loop, called exactly once — this is the opposite mistake from the permutation bug above, and just as easy to make. Creating a fresh `default_rng(seed)` on every epoch would seed the generator identically each time, so every epoch would draw the _same_ "random" permutation — reproducible, but uselessly so, since it defeats per-epoch shuffling entirely. One generator, created once, whose internal state keeps advancing across every `.permutation()` call, is what gives reproducible _and_ genuinely different-per-epoch shuffles at the same time.
