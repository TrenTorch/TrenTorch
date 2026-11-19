### Pair comparison
```cpp
struct Pair { float value; int index; };

__device__ __forceinline__ Pair better(Pair a, Pair b) {
    if (b.value > a.value) return b;
    if (b.value < a.value) return a;
    return (b.index < a.index) ? b : a;
}
```
Each thread loads a candidate `{X[i], i}` or `{-INFINITY, INT_MAX}` for an inactive lane, then reduces pairs using `better`. Use a two-stage reduction: each block writes one pair, then a final kernel reduces the partial pairs.

### Correctness details
Specify NaN behavior (ignore NaNs, propagate NaN, or follow framework semantics) and tie behavior before implementation. The comparison above assumes ordinary non-NaN values. The index is part of the reduction state; reducing only the value loses the answer.
