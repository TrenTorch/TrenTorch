#include <cuda_runtime.h>
#include <nccl.h>
#include <cstdio>

int main() {
    const int n = 4;        // GPUs
    const int count = 8;    // floats per GPU
    ncclComm_t comms[4];
    ncclCommInitAll(comms, n);

    float *d_send[4];
    float *d_recv[4];
    float h_val[8];
    for (int r = 0; r < n; r++) {
        for (int i = 0; i < count; i++) h_val[i] = (r + 1) * 1.5f;
        cudaSetDevice(r);
        cudaMalloc(&d_send[r], count * sizeof(float));
        cudaMalloc(&d_recv[r], count * sizeof(float));
        cudaMemcpy(d_send[r], h_val, count * sizeof(float), cudaMemcpyHostToDevice);
    }

    // TODO: sum d_send across all GPUs into d_recv on every GPU.

    for (int r = 0; r < n; r++) {
        cudaSetDevice(r);
        cudaMemcpy(h_val, d_recv[r], count * sizeof(float), cudaMemcpyDeviceToHost);
        printf("rank %d: %f\n", r, h_val[0]);
    }
    return 0;
}
