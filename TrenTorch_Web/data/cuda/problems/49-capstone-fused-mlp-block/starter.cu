__global__ void mlp_layer1(const float* X, const float* W1, const float* b1, float* Hid, int M, int Din, int Dh) {
    // TODO: Hid = ReLU(X * W1 + b1)
}

__global__ void mlp_layer2(const float* Hid, const float* W2, const float* b2, float* Y, int M, int Dh, int Dout) {
    // TODO: Y = Hid * W2 + b2
}
