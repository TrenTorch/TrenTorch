__global__ void mlp_layer1(const float* X, const float* W1, const float* b1, float* Hid, int M, int Din, int Dh) {
    int col = blockIdx.x * blockDim.x + threadIdx.x;
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    if (row < M && col < Dh) {
        float acc = 0.0f;
        for (int k = 0; k < Din; ++k) acc = fmaf(X[row * Din + k], W1[k * Dh + col], acc);
        Hid[row * Dh + col] = fmaxf(acc + b1[col], 0.0f);
    }
}

__global__ void mlp_layer2(const float* Hid, const float* W2, const float* b2, float* Y, int M, int Dh, int Dout) {
    int col = blockIdx.x * blockDim.x + threadIdx.x;
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    if (row < M && col < Dout) {
        float acc = 0.0f;
        for (int k = 0; k < Dh; ++k) acc = fmaf(Hid[row * Dh + k], W2[k * Dout + col], acc);
        Y[row * Dout + col] = acc + b2[col];
    }
}
