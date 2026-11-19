__global__ void conv1d(const float* x, const float* w, float* y, int N, int R) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < N) {
        float acc = 0.0f;
        for (int k = -R; k <= R; ++k) {
            int j = i + k;
            if (j >= 0 && j < N) acc = fmaf(x[j], w[k + R], acc);
        }
        y[i] = acc;
    }
}
