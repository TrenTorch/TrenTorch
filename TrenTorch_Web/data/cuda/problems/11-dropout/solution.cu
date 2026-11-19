__global__ void dropout_hash(const float* X, float* Y, int N, float keep_prob, unsigned seed) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < N) {
        // Small LCG-style hash: every product stays below 2^53, so it is exact in the simulator.
        unsigned r = ((unsigned)i * 2654435u + seed * 40503u + 12345u) % 2147483648u;
        r = (r * 1103515u + 12345u) % 2147483648u;
        float u = (float)((r / 256u) % 65536u) / 65536.0f;
        Y[i] = (u < keep_prob) ? X[i] / keep_prob : 0.0f;
    }
}
