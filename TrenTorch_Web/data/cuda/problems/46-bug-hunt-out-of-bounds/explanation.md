### Typical bug
```cpp
int i = blockIdx.x * blockDim.x + threadIdx.x;
Y[i] = X[i] * 2.0f; // invalid when i >= N
```

### Fix
```cpp
int i = blockIdx.x * blockDim.x + threadIdx.x;
if (i < N) Y[i] = X[i] * 2.0f;
```

### Checklist
- Use the correct dimension/stride when flattening multidimensional indices.
- Use `size_t` for products that may overflow 32-bit integer arithmetic.
- Check both input and output bounds for stencils and tiled kernels.
- Test sizes just below and above block/tile boundaries.
- Use Compute Sanitizer's memcheck tool.
