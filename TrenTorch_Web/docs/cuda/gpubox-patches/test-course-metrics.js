// Regression test for metrics the CUDA course depends on: divergence, coalescing,
// bank conflicts, static FLOP estimates, nested atomic addressing, T4 profile.
const G = require('../js/dist/cuda-sim.cjs.js');
let failed = 0;
const check = (name, ok, got) => { if (!ok) failed++; console.log((ok ? 'PASS ' : 'FAIL ') + name + (ok ? '' : '  got ' + got)); };
function run(src, grid, block, bufs, args, profile = 'A100') {
  const prog = G.compile(src);
  const fn = new Function('__rt', prog.transpiledCode + '; return __kernel_k;')();
  const sim = G.createSimulator({ gpuProfile: profile, raceDetection: true });
  const d = bufs.map((b) => sim.allocate(b));
  sim.launch(fn, grid, block, 0, ...args(d));
  return sim.getCounters().toJSON();
}
let c = run('__global__ void k(float a,const float* x,float* y,int n){int i=blockIdx.x*blockDim.x+threadIdx.x; if(i<n) y[i]=a*x[i]+y[i];}', 16, 256, [16384, 16384], (d) => [2, d[0], d[1], 4096]);
check('saxpy flops = 2N', c.flopCount === 8192, c.flopCount);
check('saxpy fully coalesced', c.coalescingEfficiency === 1, c.coalescingEfficiency);
check('saxpy uniform branch not divergent', c.divergentBranches === 0, c.divergentBranches);
c = run('__global__ void k(const float* a,float* o,int n){int i=blockIdx.x*blockDim.x+threadIdx.x; if(i<n){ if(i%2==0) o[i]=a[i]*2.0f; else o[i]=a[i]+1.0f; }}', 4, 256, [4096, 4096], (d) => [d[0], d[1], 1024]);
check('even/odd branch diverges in every warp', c.divergentBranches === 32, c.divergentBranches);
c = run('__global__ void k(const float* in,float* out,int W,int H){int x=blockIdx.x*blockDim.x+threadIdx.x;int y=blockIdx.y*blockDim.y+threadIdx.y; if(x<W&&y<H) out[x*H+y]=in[y*W+x];}', { x: 4, y: 4 }, { x: 16, y: 16 }, [16384, 16384], (d) => [d[0], d[1], 64, 64]);
check('naive transpose is uncoalesced', c.coalescingEfficiency < 0.5, c.coalescingEfficiency);
c = run('#define T 16\n__global__ void k(const float* A,const float* B,float* C,int N){__shared__ float As[T][T];__shared__ float Bs[T][T];int r=blockIdx.y*T+threadIdx.y,c=blockIdx.x*T+threadIdx.x;float s=0;for(int t=0;t<N/T;t++){As[threadIdx.y][threadIdx.x]=A[r*N+t*T+threadIdx.x];Bs[threadIdx.y][threadIdx.x]=B[(t*T+threadIdx.y)*N+c];__syncthreads();for(int k=0;k<T;k++)s+=As[threadIdx.y][k]*Bs[k][threadIdx.x];__syncthreads();}C[r*N+c]=s;}', { x: 4, y: 4 }, { x: 16, y: 16 }, [16384, 16384, 16384], (d) => [d[0], d[1], d[2], 64]);
check('tiled matmul flops = 2N^3', c.flopCount === 2 * 64 ** 3, c.flopCount);
check('tiled matmul has no false bank conflicts', c.bankConflicts === 0, c.bankConflicts);
c = run('__global__ void k(const int* d,int* h,int n){int i=blockIdx.x*blockDim.x+threadIdx.x; if(i<n) atomicAdd(&h[d[i]%16],1);}', 4, 256, [4096, 64], (d) => [d[0], d[1], 1024]);
check('atomicAdd(&h[d[i]%16]) compiles and counts', c.atomicOps === 1024, c.atomicOps);
c = run('__global__ void k(const float* a,float* o,int n){int i=blockIdx.x*blockDim.x+threadIdx.x; if(i<n) o[i]=a[i];}', 4, 256, [4096, 4096], (d) => [d[0], d[1], 1024], 'T4');
check('T4 profile resolves', c.estimatedTimeMs > 0, c.estimatedTimeMs);
const bank = (w) => run('__global__ void k(float* o){__shared__ float t[32][' + w + '];int x=threadIdx.x; t[x][0]=1.0f; __syncthreads(); o[x]=t[0][0];}', 1, 32, [4096], (d) => [d[0]]);
check('t[x][0] on [32][32] is a 32-way conflict', bank(32).bankConflicts === 31, bank(32).bankConflicts);
check('padding to [32][33] removes the conflict', bank(33).bankConflicts === 0, bank(33).bankConflicts);

// ---- C++ semantics the course kernels rely on ----
const vals = (src, grid, block, n, args) => { const sim = G.createSimulator({ gpuProfile: 'A100' }); const prog = G.compile(src); const fn = new Function('__rt', prog.transpiledCode + '; return __kernel_k;')(); const q = sim.allocate(n * 4); sim.launch(fn, grid, block, 0, q, ...args); const o = new Float32Array(n); sim.memcpy(o, q, n * 4, 'D2H'); return Array.from(o); };
let v = vals('#define T 4\n__global__ void k(float* y,int K){int cnt=0;for(int t=0;t<(K+T-1)/T;++t)cnt++;y[0]=cnt;y[1]=(float)K/4;y[2]=K/4;float f=7/2;y[3]=f;y[4]=(int)(K*0.5f)/2;}', 1, 1, 5, [6]);
check('integer division truncates, casts respected', v.join() === '2,1.5,1,3,1', v.join());
v = vals('__global__ void k(float* y){unsigned h=5u;constexpr float c=2.0f;y[0]=h*c+erff(0.0f)+(CUDART_INF_F>1.0f?1.0f:0.0f);y[1]=(float)(0xffu);}', 1, 1, 2, []);
check('u suffix, constexpr, erff, CUDART_INF_F', v.join() === '11,255', v.join());
v = vals('__global__ void k(float* y){float4 a=make_float4(1.0f,2.0f,3.0f,4.0f);float4 b;b.x=a.w;reinterpret_cast<float4*>(y)[0]=b;}', 1, 1, 4, []);
check('float4 store', v[0] === 4, v.join());
c = run('__global__ void k(const float* X,float* Y,int N){int v=blockIdx.x*blockDim.x+threadIdx.x;if(v<N/4){const float4 x=reinterpret_cast<const float4*>(X)[v];float4 y;y.x=fmaxf(x.x,0.0f);y.y=fmaxf(x.y,0.0f);y.z=fmaxf(x.z,0.0f);y.w=fmaxf(x.w,0.0f);reinterpret_cast<float4*>(Y)[v]=y;}}', 1, 64, [1024, 1024], (d) => [d[0], d[1], 256]);
check('float4 load/store is 16 bytes and fully coalesced', c.globalLoads === 64 && c.globalLoadBytes === 1024 && c.coalescingEfficiency === 1, JSON.stringify([c.globalLoads, c.globalLoadBytes, c.coalescingEfficiency]));

// ---- dynamic shared memory, shared atomics, float4 with an offset, NCCL order mismatch ----
{
  const sim = G.createSimulator({ gpuProfile: 'A100' });
  const prog = G.compile('__global__ void c(float* o){ extern __shared__ float s[]; int t=threadIdx.x; int n=blockDim.x; s[n+t]=t; s[2*n+t]=2*t; __syncthreads(); o[t]=s[n+t]+s[2*n+t]; } __global__ void h(unsigned* hist){ __shared__ unsigned local[8]; local[threadIdx.x]=0; __syncthreads(); atomicAdd(&local[threadIdx.x%2], 1); __syncthreads(); if(threadIdx.x<2) atomicAdd(&hist[threadIdx.x], local[threadIdx.x]); } __global__ void v(const float* B,float* C,int N){int c=threadIdx.x;float4 b=reinterpret_cast<const float4*>(B + 4 * N)[c];reinterpret_cast<float4*>(C + 4 * N)[c]=b;}');
  const fns = new Function('__rt', prog.transpiledCode + ';return {c:__kernel_c,h:__kernel_h,v:__kernel_v};')();
  const q = sim.allocate(64); sim.launch(fns.c, 1, 4, 48, q); let o = new Float32Array(4); sim.memcpy(o, q, 16, 'D2H');
  check('extern __shared__ uses the launch size (3 x 4 floats)', o.join() === '0,3,6,9', o.join());
  const q2 = sim.allocate(16); sim.launch(fns.h, 2, 8, 0, q2); o = new Float32Array(2); sim.memcpy(o, q2, 8, 'D2H');
  check('atomicAdd on a static __shared__ array', o.join() === '8,8', o.join());
  const B = sim.allocate(64), C = sim.allocate(64); sim.memcpy(B, Float32Array.from({ length: 16 }, (_, i) => i), 64, 'H2D'); sim.launch(fns.v, 1, 1, 0, B, C, 1);
  o = new Float32Array(16); sim.memcpy(o, C, 64, 'D2H');
  check('float4 access through P + offset', o.slice(4, 8).join() === '4,5,6,7', o.join());
}
{
  const nccl = (second) => `#include <cuda_runtime.h>
#include <nccl.h>
int main() { ncclComm_t comms[2]; ncclCommInitAll(comms, 2); float *a[2]; float *b[2];
  for (int r = 0; r < 2; r++) { cudaSetDevice(r); cudaMalloc(&a[r], 16); cudaMalloc(&b[r], 16); }
  for (int r = 0; r < 2; r++) { cudaSetDevice(r);
    if (r == 0 || ${second}) { ncclAllReduce(a[r], b[r], 4, ncclFloat, ncclSum, comms[r], 0); ncclBroadcast(b[r], b[r], 4, ncclFloat, 0, comms[r], 0); }
    else { ncclBroadcast(b[r], b[r], 4, ncclFloat, 0, comms[r], 0); ncclAllReduce(a[r], b[r], 4, ncclFloat, ncclSum, comms[r], 0); } }
  return 0; }`;
  const bug = G.run(nccl('0'), { gpuProfile: 'A100', numDevices: 2 }), ok = G.run(nccl('1'), { gpuProfile: 'A100', numDevices: 2 });
  check('NCCL order mismatch is reported', bug.status === 'ERROR' && bug.diagnostics.some((d) => d.type === 'NcclDesyncError'), bug.status);
  check('matching NCCL order passes', ok.status === 'PASS', ok.status + JSON.stringify(ok.diagnostics).slice(0, 120));
}

c = run('#define T 16\n__global__ void k(const float* A,float* C){__shared__ float As[T][T];__shared__ float Bs[T][T];As[threadIdx.y][threadIdx.x]=A[threadIdx.y*T+threadIdx.x];Bs[threadIdx.y][threadIdx.x]=A[threadIdx.y*T+threadIdx.x];__syncthreads();float acc=0.0f;for(int k=0;k<T;++k)acc=fmaf(As[threadIdx.y][k],Bs[k][threadIdx.x],acc);C[threadIdx.y*T+threadIdx.x]=acc;}', 1, { x: 16, y: 16 }, [1024, 1024], (d) => [d[0], d[1]]);
check('fmaf on shared-array operands counts FLOPs (2 per k per thread)', c.flopCount === 2 * 16 * 256, c.flopCount);
process.exit(failed ? 1 : 0);
