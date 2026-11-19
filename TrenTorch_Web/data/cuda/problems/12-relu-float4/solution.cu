__global__ void relu_float4(const float* X, float* Y, int N) {
    int v = blockIdx.x * blockDim.x + threadIdx.x;
    int vec_count = N / 4;
    if (v < vec_count) {
        float4 x = reinterpret_cast<const float4*>(X)[v];
        float4 y;
        y.x = fmaxf(x.x, 0.0f);
        y.y = fmaxf(x.y, 0.0f);
        y.z = fmaxf(x.z, 0.0f);
        y.w = fmaxf(x.w, 0.0f);
        reinterpret_cast<float4*>(Y)[v] = y;
    }
    // Tail: threads 0..(N % 4 - 1) handle the last elements.
    int i = vec_count * 4 + v;
    if (i < N) Y[i] = fmaxf(X[i], 0.0f);
}
