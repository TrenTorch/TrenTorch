### Fused epilogue
In CU-032's output path, replace the final store with:
```cpp
if (row < M && col < N) {
    float v = acc + bias[col];   // for column-broadcast bias
    C[(size_t)row*N+col] = fmaxf(v, 0.0f);
}
```

### Why fuse
A separate bias kernel and ReLU kernel would read and write the full output multiple times. Fusion performs the epilogue while the accumulator is already in registers, eliminating intermediate global-memory round trips and launches. For production GEMM, use a library epilogue or CUTLASS-style fused epilogue where available.

---
