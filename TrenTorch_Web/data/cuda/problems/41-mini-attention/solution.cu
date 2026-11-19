__global__ void attention(const float* Q, const float* Kmat, const float* V, float* O, int T, int D) {
    __shared__ float q[64];
    __shared__ float scores[64];
    int row = blockIdx.x;
    int t = threadIdx.x;

    if (t < D) q[t] = Q[row * D + t];
    __syncthreads();

    // one score per thread
    float sc = -INFINITY;
    if (t < T) {
        float dot = 0.0f;
        for (int d = 0; d < D; ++d) dot += q[d] * Kmat[t * D + d];
        sc = dot / sqrtf((float)D);
    }
    scores[t] = sc;
    __syncthreads();

    // stable softmax across the row (thread 0 reduces; T <= 64 keeps this tiny)
    __shared__ float stats[2];
    if (t == 0) {
        float m = -INFINITY;
        for (int j = 0; j < T; ++j) m = fmaxf(m, scores[j]);
        float sum = 0.0f;
        for (int j = 0; j < T; ++j) sum += expf(scores[j] - m);
        stats[0] = m;
        stats[1] = sum;
    }
    __syncthreads();
    if (t < T) scores[t] = expf(scores[t] - stats[0]) / stats[1];
    __syncthreads();

    // weighted sum of V rows: thread t owns output dimension t
    if (t < D) {
        float acc = 0.0f;
        for (int j = 0; j < T; ++j) acc += scores[j] * V[j * D + t];
        O[row * D + t] = acc;
    }
}
