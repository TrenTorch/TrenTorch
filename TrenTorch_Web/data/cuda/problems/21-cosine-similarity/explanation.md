### Fused accumulation
Each thread accumulates three values while traversing its assigned elements:
```cpp
float dot = 0.f, aa = 0.f, bb = 0.f;
for (int i = start; i < n; i += stride) {
    float a = A[i], b = B[i];
    dot = fmaf(a, b, dot);
    aa = fmaf(a, a, aa);
    bb = fmaf(b, b, bb);
}
```
Reduce a three-float tuple within each block, write one partial tuple per block, then reduce the partial tuples. Finally compute `dot * rsqrtf(aa) * rsqrtf(bb)`.

### Why fuse
A fused pass reads `A` and `B` once instead of performing separate dot and norm passes. This reduces input traffic, though each thread maintains three accumulators and the reduction state is larger. Handle zero norms and numerical tolerance explicitly.

---
