### Kernel
```cpp
__global__ void swish(const float* X, float* Y, int N) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < N) {
        float x = X[i];
        Y[i] = x / (1.0f + expf(-x));
    }
}
```

### Why fuse
A separate sigmoid kernel followed by a multiply kernel would materialize an intermediate and add launches and memory traffic. Computing both in one kernel reads `X` once and writes `Y` once. The exponential raises arithmetic cost; large inputs may be math-throughput-limited.
