# Row-wise ops: softmax, normalization, loss

## Shape of the problem

Given a matrix of `rows × cols`, do the same reduction-then-map **independently for each row**. Natural mapping: **one block per row** (or one warp per row if rows are short). Threads in the block stride across the row, reduce, then stride across it again to write.

## Stable softmax

$\text{softmax}(x)_j = e^{x_j} / \sum_k e^{x_k}$ overflows for large $x$. Subtract the row max first; the result is identical but the exponent is never positive. Steps per row: (1) max-reduce, (2) sum of $e^{x - m}$, (3) divide. That reads the row three times.

## Online softmax: one pass

Keep a running max $m$ and running sum $d$. When a new value $x$ arrives:
$$m' = \max(m, x), \qquad d' = d \cdot e^{m - m'} + e^{x - m'}$$
Two partial states $(m_1, d_1)$ and $(m_2, d_2)$ merge with the same rule, so each thread keeps its own state and the block combines them with a reduction. This is the core trick behind fused attention (F3).

## LayerNorm and RMSNorm

- **LayerNorm:** subtract the row mean, divide by $\sqrt{\text{var} + \epsilon}$, then scale and shift.
- **RMSNorm:** divide by $\sqrt{\text{mean}(x^2) + \epsilon}$; no mean subtraction.
Compute the sums in one pass. The shortcut $\text{var} = E[x^2] - E[x]^2$ can lose precision when the mean is large; **Welford's** running update (or a two-pass method) is safer. `rsqrtf` gives $1/\sqrt{\cdot}$ cheaply.

## Cross-entropy

For logits $z$ and target class $t$: loss $= \log\sum_k e^{z_k} - z_t$. The log-sum-exp is a stable softmax denominator. Reduce per row, then optionally average across rows.

## Memory view

These kernels are memory-bound. The goal is to touch each row's data as few times as possible: three reads is the baseline, one (online) is the target. The optimality certificate counts bytes against that lower bound.

## Interactive: One block per row

<div class="cuda-viz" data-viz="VIZ-ROWWISE-SOFTMAX" data-title="One block per row" data-spec="VIZ-ROWWISE-SOFTMAX"></div>

## Does the row fit on-chip?

If a row of `C` floats fits in registers/shared memory (C ≲ 4K-8K floats per block in practice), load it **once** and do all three softmax passes on-chip: global bytes = 4C read + 4C write = 8C, which is already the lower bound. The online algorithm only matters when the row does **not** fit. Example: an LM-head softmax over a 50,257-token vocabulary = 201 KB per row, which exceeds the 164 KB shared memory on A100, so it needs the online (streaming) formulation (or splitting across a block + cluster).

## Online softmax: why the merge is correct

State (m, d) represents `d = Σ e^{x_j − m}` over the processed elements. Merge two states: with M = max(m₁, m₂),
$$d = d_1 e^{m_1 - M} + d_2 e^{m_2 - M}.$$
Each term rescales a sum "as if its max had been M", so the merged state equals the state you would get by processing all elements sequentially. Numeric check: (m₁,d₁) = (2,3) and (m₂,d₂) = (5,1) → M = 5, d = 3e⁻³ + 1 = 1.149.

## Welford and Chan's parallel merge for variance

Per-thread state (n, μ, M₂) with M₂ = Σ(x−μ)². Merge:
$$n = n_a+n_b,\quad \delta = \mu_b-\mu_a,\quad \mu = \mu_a + \delta\frac{n_b}{n},\quad M_2 = M_{2a}+M_{2b}+\delta^2\frac{n_a n_b}{n}.$$
Variance = M₂/n (or n−1). No catastrophic cancellation, and the same merge works at every level of the block tree. Show failure of the naive `E[x²]−E[x]²`: values 10⁸ + {1,2,3}: in FP32 the squares are ~10¹⁶ with spacing ~10⁹, so the variance computed this way is **garbage (often 0 or negative)** while the true variance is 2/3.

## Cross-entropy fused with softmax

Never materialize probabilities when you only need the loss: `loss = (m + log d) − z_t` from the online state. For a batch of 4,096 rows × 50,257 classes, skipping the probability matrix saves 823 MB of writes and reads per pass (4,096 × 50,257 × 4 B ≈ 823 MB).

## Check yourself

1. Why does subtracting the max not change the softmax result?
2. Merge (m=2, d=3) with (m=5, d=1). What are the new m and d?
3. When can $E[x^2]-E[x]^2$ be badly wrong?
4. Bytes moved by a row-resident softmax of C = 4,096 floats (per row)?
5. Chan-merge two groups: (n=2, μ=1, M₂=2) and (n=2, μ=5, M₂=2). Result?
6. Why is fusing cross-entropy with softmax a memory win?

<details class="answers">
<summary>Show answers</summary>

1. the common factor e^{−m} cancels.
2. m = 5, d = 1.149.
3. when |mean| ≫ std.
4. 4C + 4C = 32 KB (16 KB read + 16 KB write).
5. n = 4, μ = 3, M₂ = 2 + 2 + 16·(2·2/4) = 20.
6. no probability matrix is written.

</details>

## Practice

[CU-022 Softmax](problem:CU-022) · [CU-023 RMS Norm](problem:CU-023) · [CU-024 Layer Norm](problem:CU-024) · [CU-025 Cross-Entropy](problem:CU-025)

*PMPP reference:* Ch. 10 (reduction patterns used inside row-wise kernels), Ch. 16 (deep learning kernels: softmax, normalization as used in networks). *Online softmax / FlashAttention: not in PMPP; cite Milakov & Gimelshein (2018) and Dao et al. (2022) in "Further reading".*

## Further reading

- Milakov & Gimelshein, "Online normalizer calculation for softmax" (2018); Dao et al., "FlashAttention" (2022)
