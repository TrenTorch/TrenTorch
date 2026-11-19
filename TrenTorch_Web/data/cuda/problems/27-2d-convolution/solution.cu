__global__ void conv2d(const float* X, const float* F, float* Y, int H, int W, int FH, int FW) {
    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;
    if (x >= W || y >= H) return;
    int rx = FW / 2, ry = FH / 2;
    float acc = 0.0f;
    for (int ky = 0; ky < FH; ++ky) {
        for (int kx = 0; kx < FW; ++kx) {
            int ix = x + kx - rx, iy = y + ky - ry;
            if (ix >= 0 && ix < W && iy >= 0 && iy < H) acc = fmaf(X[iy * W + ix], F[ky * FW + kx], acc);
        }
    }
    Y[y * W + x] = acc;
}
