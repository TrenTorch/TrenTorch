#include <cuda_runtime.h>
#include <nccl.h>
#include <cstdio>

int main() {
    const int n = 4;          // GPUs
    const int shard = 2;      // elements each rank keeps
    ncclComm_t comms[4];
    ncclCommInitAll(comms, n);

    float *d_send[4];
    float *d_recv[4];
    float h_val[8];
    for (int r = 0; r < n; r++) {
        for (int i = 0; i < n * shard; i++) h_val[i] = (r + 1) * (i + 1);
        cudaSetDevice(r);
        cudaMalloc(&d_send[r], n * shard * sizeof(float));
        cudaMalloc(&d_recv[r], shard * sizeof(float));
        cudaMemcpy(d_send[r], h_val, n * shard * sizeof(float), cudaMemcpyHostToDevice);
    }

    // TODO: sum across ranks and scatter: rank k keeps elements k*shard .. k*shard+shard-1 of the sum.

    float h_out[2];
    for (int r = 0; r < n; r++) {
        cudaSetDevice(r);
        cudaMemcpy(h_out, d_recv[r], shard * sizeof(float), cudaMemcpyDeviceToHost);
        printf("rank %d: %f %f\n", r, h_out[0], h_out[1]);
    }
    return 0;
}
