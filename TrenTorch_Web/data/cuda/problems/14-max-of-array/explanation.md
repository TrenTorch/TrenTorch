### Problem and kernel pattern
Use the same two-stage structure as CU-013, replacing addition with `fmaxf` and the identity with negative infinity:
```cpp
float v = (i < N) ? X[i] : -CUDART_INF_F;
s[t] = v;
// tree step:
if (t < d) s[t] = fmaxf(s[t], s[t + d]);
```
The final stage also uses `-CUDART_INF_F` for inactive lanes.

### Atomic caveat
Native `atomicMax` support for floating point depends on architecture/toolkit and API. Integer reinterpretation tricks are valid only under carefully stated value assumptions and ordering transformations; they are not a general solution for arbitrary NaNs and signed values. A two-stage reduction is portable and easy to reason about.
