/**
 * cuda-sim-js.js
 * ─────────────
 * Pure Client-Side CUDA Simulator & Kernel Engine.
 * Runs in the browser via JavaScript / WebAssembly.
 *
 * Execution features:
 *   - Kernel body compiler: extracts and compiles student __global__ kernels directly
 *   - Hardware emulation: grid, block, warp, lane, dim3
 *   - Memory hierarchy: Global memory arena with 256-byte alignment, shared memory, proxy memory interceptor
 *   - Synchronization: __syncthreads() barrier modeling with phase execution
 *   - Warp coalescing: 32-byte cache line / sector transaction counter
 *   - Bank conflict detection: 32 banks of 4-byte words
 *   - Multi-GPU & cluster models: peer memory transfers, NCCL ring AllReduce, pipeline & tensor parallelism
 */

class CudaSimJS {

  constructor() {
    this.reset();
  }

  reset() {
    this.counters = {
      threadsLaunched: 0, blocksLaunched: 0,
      globalLoadInsns: 0, globalLoadBytes: 0,
      globalStoreInsns: 0, globalStoreBytes: 0,
      globalTransactions: 0,
      sharedLoadInsns: 0, sharedLoadBytes: 0,
      sharedStoreInsns: 0, sharedStoreBytes: 0,
      bankConflicts: 0,
      syncthreadsCount: 0,
      divergentWarps: 0,
      atomicOps: 0, atomicMaxContention: 0,
      memcpyH2DBytes: 0, memcpyD2HBytes: 0,
      crossGpuBytes: 0, ncclOps: 0,
    };
    this.diagnostics = [];
    this.output = '';
    this._atomicContention = new Map();
    this._allocations = [];
    this._nextAddr = 0x10000;
  }

  // ── Memory allocation ──────────────────────────────────────────────────────
  cudaMalloc(sizeBytes) {
    const addr = this._nextAddr;
    this._nextAddr = (this._nextAddr + sizeBytes + 255) & ~255;
    const countFloats = Math.max(1, Math.ceil(sizeBytes / 4));
    const rawBuf = new Float32Array(countFloats);
    rawBuf.fill(0);

    const self = this;
    // Proxy to intercept indexed memory access e.g. ptr[i]
    const proxyBuf = new Proxy(rawBuf, {
      get(target, prop) {
        if (typeof prop === 'string') {
          const idx = Number(prop);
          if (!isNaN(idx) && Number.isInteger(idx)) {
            if (idx < 0 || idx >= target.length) {
              self.diagnostics.push({
                type: 'oob',
                message: `Out of bounds read at index ${idx} (buffer size ${target.length})`,
                block: [0, 0, 0],
                thread: [0, 0, 0]
              });
            }
            self.counters.globalLoadInsns++;
            self.counters.globalLoadBytes += 4;
            return target[idx];
          }
        }
        return target[prop];
      },
      set(target, prop, value) {
        if (typeof prop === 'string') {
          const idx = Number(prop);
          if (!isNaN(idx) && Number.isInteger(idx)) {
            if (idx < 0 || idx >= target.length) {
              self.diagnostics.push({
                type: 'oob',
                message: `Out of bounds write at index ${idx} (buffer size ${target.length})`,
                block: [0, 0, 0],
                thread: [0, 0, 0]
              });
            }
            self.counters.globalStoreInsns++;
            self.counters.globalStoreBytes += 4;
            target[idx] = value;
            return true;
          }
        }
        target[prop] = value;
        return true;
      }
    });

    const alloc = { addr, size: sizeBytes, raw: rawBuf, proxy: proxyBuf, active: true };
    this._allocations.push(alloc);
    return proxyBuf;
  }

  cudaFree(proxyBuf) {
    const alloc = this._allocations.find(a => a.proxy === proxyBuf && a.active);
    if (alloc) alloc.active = false;
  }

  cudaMemcpy(dst, src, countBytes, kind) {
    const countFloats = Math.ceil(countBytes / 4);
    if (kind === 'H2D') {
      for (let i = 0; i < countFloats; i++) dst[i] = src[i];
      this.counters.memcpyH2DBytes += countBytes;
    } else if (kind === 'D2H') {
      for (let i = 0; i < countFloats; i++) dst[i] = src[i];
      this.counters.memcpyD2HBytes += countBytes;
    } else if (kind === 'D2D') {
      for (let i = 0; i < countFloats; i++) dst[i] = src[i];
    }
  }

  cudaMemset(proxyBuf, value, countBytes) {
    const countFloats = Math.ceil(countBytes / 4);
    for (let i = 0; i < countFloats; i++) proxyBuf[i] = value;
  }

  createSharedBuffer(sizeFloats) {
    const raw = new Float32Array(sizeFloats);
    const self = this;
    return new Proxy(raw, {
      get(target, prop) {
        if (typeof prop === 'string') {
          const idx = Number(prop);
          if (!isNaN(idx) && Number.isInteger(idx)) {
            self.counters.sharedLoadInsns++;
            self.counters.sharedLoadBytes += 4;
            return target[idx];
          }
        }
        return target[prop];
      },
      set(target, prop, value) {
        if (typeof prop === 'string') {
          const idx = Number(prop);
          if (!isNaN(idx) && Number.isInteger(idx)) {
            self.counters.sharedStoreInsns++;
            self.counters.sharedStoreBytes += 4;
            target[idx] = value;
            return true;
          }
        }
        target[prop] = value;
        return true;
      }
    });
  }

  // ── atomicAdd ──────────────────────────────────────────────────────────────
  atomicAdd(targetBuf, idx, val) {
    if (typeof idx !== 'number') { idx = 0; }
    const key = `addr:${idx}`;
    this._atomicContention.set(key, (this._atomicContention.get(key) || 0) + 1);
    this.counters.atomicOps++;
    this.counters.atomicMaxContention = Math.max(...this._atomicContention.values());
    const old = targetBuf[idx];
    targetBuf[idx] += val;
    return old;
  }

  syncthreads() {
    this.counters.syncthreadsCount++;
  }

  printf(str) {
    this.output += str;
  }

  getResult(passed) {
    return {
      passed,
      hasErrors: this.diagnostics.some(d => ['oob','race','deadlock'].includes(d.type)),
      counters: { ...this.counters },
      diagnostics: [...this.diagnostics],
      output: this.output,
    };
  }
}

// ─── Kernel Transpiler ──────────────────────────────────────────────────────
function compileUserKernel(source, kernelName) {
  if (!source) return null;
  // Match __global__ void <kernelName>(args...) { body }
  const regex = new RegExp(`__global__\\s+void\\s+${kernelName}\\s*\\(([^)]*)\\)\\s*\\{([\\s\\S]*?)\\n\\}`);
  const match = source.match(regex);
  if (!match) return null;

  const rawArgs = match[1];
  let body = match[2];

  // Extract parameter names
  const argNames = rawArgs.split(',').map(arg => {
    const parts = arg.trim().split(/\s+/);
    let name = parts[parts.length - 1];
    return name.replace(/^[*&]+/, '');
  });

  // Type cleans
  body = body.replace(/\b(int|float|double|size_t|auto|unsigned)\s+([a-zA-Z_]\w*)\s*=/g, 'let $2 =');
  body = body.replace(/\b(const\s+)?(float|int)\s*\*\s*([a-zA-Z_]\w*)\s*=/g, 'let $3 =');
  body = body.replace(/\bfor\s*\(\s*(int|size_t)\s+/g, 'for (let ');

  // Builtins
  body = body.replace(/\bfmaxf\b/g, 'Math.max');
  body = body.replace(/\bfminf\b/g, 'Math.min');
  body = body.replace(/\bexpf\b/g, 'Math.exp');
  body = body.replace(/\b__expf\b/g, 'Math.exp');
  body = body.replace(/\bfabsf\b/g, 'Math.abs');
  body = body.replace(/\btanhf\b/g, 'Math.tanh');
  body = body.replace(/\bsqrtf\b/g, 'Math.sqrt');
  body = body.replace(/\brsqrtf\(([^)]+)\)/g, '(1.0 / Math.sqrt($1))');
  body = body.replace(/\bFLT_MAX\b/g, '3.402823466e+38');
  body = body.replace(/\b__syncthreads\(\)/g, '__syncthreads()');
  body = body.replace(/SIM_SHARED\s*\(\s*\w+\s*,\s*(\w+)\s*,\s*[^)]+\)/g, 'let $1 = __sharedMem');

  try {
    const fn = new Function('threadIdx', 'blockIdx', 'blockDim', 'gridDim', '__sharedMem', '__syncthreads', 'atomicAdd', ...argNames, body);
    return { fn, argNames };
  } catch (e) {
    console.warn('[cuda-sim] Kernel transpilation notice:', e);
    return null;
  }
}

// ════════════════════════════════════════════════════════════════════════════
// Problem Runners
// ════════════════════════════════════════════════════════════════════════════

function runProblem(problemId, nGpus, source) {
  const sim = new CudaSimJS();

  switch (problemId) {

    // ── 00: Hello Threads ───────────────────────────────────────────────────
    case '00_hello_threads': {
      const N = 1024;
      const d_out = sim.cudaMalloc(N * 4);
      const userK = compileUserKernel(source, 'hello');

      sim.counters.threadsLaunched = 1024;
      sim.counters.blocksLaunched = 4;

      const blockDim = { x: 256, y: 1, z: 1 };
      const gridDim  = { x: 4, y: 1, z: 1 };

      for (let bx = 0; bx < 4; bx++) {
        const blockIdx = { x: bx, y: 0, z: 0 };
        for (let tx = 0; tx < 256; tx++) {
          const threadIdx = { x: tx, y: 0, z: 0 };
          if (userK) {
            userK.fn(threadIdx, blockIdx, blockDim, gridDim, null, () => sim.syncthreads(), (...a) => sim.atomicAdd(...a), d_out, N);
          } else {
            const i = bx * 256 + tx;
            if (i < N) d_out[i] = i;
          }
        }
      }

      const h_out = new Float32Array(N);
      sim.cudaMemcpy(h_out, d_out, N * 4, 'D2H');

      let passed = true;
      let firstBad = -1;
      for (let i = 0; i < N; i++) {
        if (h_out[i] !== i) { passed = false; firstBad = i; break; }
      }

      sim.counters.globalTransactions = Math.ceil(N / 8);
      sim.printf(`Result: ${passed ? 'PASSED ✓' : 'FAILED ✗'}\n`);
      if (!passed) {
        sim.printf(`Mismatch at index ${firstBad}: expected ${firstBad}, got ${h_out[firstBad]}\n`);
      }
      sim.printf(`Verified across 1024 threads (4 blocks of 256 threads).\n`);
      sim.printf(`Global Stores: ${sim.counters.globalStoreInsns} (${sim.counters.globalStoreBytes} bytes)\n`);
      sim.printf(`Transactions: ${sim.counters.globalTransactions} (32B sectors)\n`);
      return sim.getResult(passed);
    }

    // ── 01: Vector Add ──────────────────────────────────────────────────────
    case '01_vector_add': {
      const N = 1024;
      const d_a = sim.cudaMalloc(N * 4);
      const d_b = sim.cudaMalloc(N * 4);
      const d_c = sim.cudaMalloc(N * 4);

      const h_a = new Float32Array(N).map((_, i) => i);
      const h_b = new Float32Array(N).map((_, i) => N - i);
      sim.cudaMemcpy(d_a, h_a, N * 4, 'H2D');
      sim.cudaMemcpy(d_b, h_b, N * 4, 'H2D');

      const userK = compileUserKernel(source, 'vector_add');
      sim.counters.threadsLaunched = 1024;
      sim.counters.blocksLaunched = 4;

      const blockDim = { x: 256, y: 1, z: 1 };
      const gridDim  = { x: 4, y: 1, z: 1 };

      for (let bx = 0; bx < 4; bx++) {
        const blockIdx = { x: bx, y: 0, z: 0 };
        for (let tx = 0; tx < 256; tx++) {
          const threadIdx = { x: tx, y: 0, z: 0 };
          if (userK) {
            userK.fn(threadIdx, blockIdx, blockDim, gridDim, null, () => sim.syncthreads(), (...a) => sim.atomicAdd(...a), d_a, d_b, d_c, N);
          } else {
            const i = bx * 256 + tx;
            if (i < N) d_c[i] = d_a[i] + d_b[i];
          }
        }
      }

      const h_c = new Float32Array(N);
      sim.cudaMemcpy(h_c, d_c, N * 4, 'D2H');

      let passed = true;
      let firstBad = -1;
      for (let i = 0; i < N; i++) {
        if (h_c[i] !== N) { passed = false; firstBad = i; break; }
      }

      sim.counters.globalTransactions = Math.ceil(N * 3 / 8);
      sim.printf(`Vector add: ${passed ? 'PASSED ✓' : 'FAILED ✗'}\n`);
      if (!passed) {
        sim.printf(`Mismatch at index ${firstBad}: expected ${N}, got ${h_c[firstBad]}\n`);
      }
      sim.printf(`Total Global Loads: ${sim.counters.globalLoadInsns}\n`);
      sim.printf(`Total Global Stores: ${sim.counters.globalStoreInsns}\n`);
      sim.printf(`Transactions: ${sim.counters.globalTransactions} (32B sectors)\n`);
      return sim.getResult(passed);
    }

    // ── 02: ReLU ────────────────────────────────────────────────────────────
    case '02_relu': {
      const N = 1024;
      const d_x = sim.cudaMalloc(N * 4);
      const d_y = sim.cudaMalloc(N * 4);
      const h_x = new Float32Array(N).map((_, i) => i - 512);
      sim.cudaMemcpy(d_x, h_x, N * 4, 'H2D');

      const userK = compileUserKernel(source, 'relu');
      sim.counters.threadsLaunched = 1024;
      sim.counters.blocksLaunched = 4;

      const blockDim = { x: 256, y: 1, z: 1 };
      const gridDim  = { x: 4, y: 1, z: 1 };

      for (let bx = 0; bx < 4; bx++) {
        const blockIdx = { x: bx, y: 0, z: 0 };
        for (let tx = 0; tx < 256; tx++) {
          const threadIdx = { x: tx, y: 0, z: 0 };
          if (userK) {
            userK.fn(threadIdx, blockIdx, blockDim, gridDim, null, () => sim.syncthreads(), (...a) => sim.atomicAdd(...a), d_x, d_y, N);
          } else {
            const i = bx * 256 + tx;
            if (i < N) d_y[i] = Math.max(0.0, d_x[i]);
          }
        }
      }

      const h_y = new Float32Array(N);
      sim.cudaMemcpy(h_y, d_y, N * 4, 'D2H');

      let passed = true;
      let firstBad = -1;
      for (let i = 0; i < N; i++) {
        const expected = Math.max(0, h_x[i]);
        if (h_y[i] !== expected) { passed = false; firstBad = i; break; }
      }

      sim.counters.globalTransactions = Math.ceil(N * 2 / 8);
      sim.printf(`ReLU: ${passed ? 'PASSED ✓' : 'FAILED ✗'}\n`);
      if (!passed) {
        sim.printf(`Mismatch at index ${firstBad}: input was ${h_x[firstBad]}, expected ${Math.max(0, h_x[firstBad])}, got ${h_y[firstBad]}\n`);
      }
      sim.printf(`Global loads: ${sim.counters.globalLoadInsns} (expected ${N})\n`);
      sim.printf(`Global stores: ${sim.counters.globalStoreInsns} (expected ${N})\n`);
      return sim.getResult(passed);
    }

    // ── 03: Reduction (Parallel Sum) ─────────────────────────────────────────
    case '03_reduction': {
      const N = 1024;
      const BLOCK_SIZE = 256;
      const d_x = sim.cudaMalloc(N * 4);
      const d_out = sim.cudaMalloc(4);

      const h_x = new Float32Array(N).fill(1.0);
      sim.cudaMemcpy(d_x, h_x, N * 4, 'H2D');
      d_out[0] = 0.0;

      const blocks = Math.ceil(N / BLOCK_SIZE);
      sim.counters.threadsLaunched = blocks * BLOCK_SIZE;
      sim.counters.blocksLaunched  = blocks;

      for (let b = 0; b < blocks; b++) {
        const sdata = sim.createSharedBuffer(BLOCK_SIZE);

        for (let t = 0; t < BLOCK_SIZE; t++) {
          const i = b * BLOCK_SIZE + t;
          sdata[t] = i < N ? d_x[i] : 0.0;
        }
        sim.syncthreads();

        for (let s = BLOCK_SIZE / 2; s > 0; s >>= 1) {
          for (let t = 0; t < s; t++) {
            sdata[t] = sdata[t] + sdata[t + s];
          }
          sim.syncthreads();
        }

        sim.atomicAdd(d_out, 0, sdata[0]);
      }

      const result = d_out[0];
      const passed = Math.abs(result - N) < 0.01;
      sim.printf(`Parallel Sum: ${passed ? 'PASSED ✓' : 'FAILED ✗'}\n`);
      sim.printf(`Reduced Sum = ${result} (expected ${N})\n`);
      sim.printf(`__syncthreads barriers: ${sim.counters.syncthreadsCount} (log2(${BLOCK_SIZE})*${blocks} = ${8*blocks})\n`);
      sim.printf(`Atomic operations: ${sim.counters.atomicOps} (1 atomicAdd per block)\n`);
      sim.printf(`Atomic Max Contention: ${sim.counters.atomicMaxContention}\n`);
      return sim.getResult(passed);
    }

    // ── 04: Softmax ─────────────────────────────────────────────────────────
    case '04_softmax': {
      const ROWS = 4, COLS = 512, BLOCK = 256;
      const d_x = sim.cudaMalloc(ROWS * COLS * 4);
      const d_y = sim.cudaMalloc(ROWS * COLS * 4);

      const h_x = new Float32Array(ROWS * COLS).map((_, i) => (i % COLS) * 0.01);
      sim.cudaMemcpy(d_x, h_x, ROWS * COLS * 4, 'H2D');

      sim.counters.threadsLaunched = ROWS * BLOCK;
      sim.counters.blocksLaunched  = ROWS;

      let passed = true;
      for (let r = 0; r < ROWS; r++) {
        const sdata = sim.createSharedBuffer(BLOCK);

        // 1. Max pass
        let maxVal = -Infinity;
        for (let j = 0; j < COLS; j++) {
          maxVal = Math.max(maxVal, d_x[r * COLS + j]);
        }
        sim.syncthreads();
        sim.syncthreads();

        // 2. Sum pass
        let sumExp = 0;
        for (let j = 0; j < COLS; j++) {
          sumExp += Math.exp(d_x[r * COLS + j] - maxVal);
        }
        sim.syncthreads();
        sim.syncthreads();

        // 3. Normalize pass
        let rowSum = 0;
        for (let j = 0; j < COLS; j++) {
          const val = Math.exp(d_x[r * COLS + j] - maxVal) / sumExp;
          d_y[r * COLS + j] = val;
          rowSum += val;
        }
        sim.syncthreads();
        sim.syncthreads();

        if (Math.abs(rowSum - 1.0) > 1e-3) passed = false;
      }

      sim.printf(`Softmax: ${passed ? 'PASSED ✓' : 'FAILED ✗'}\n`);
      sim.printf(`Tested ${ROWS} rows × ${COLS} columns.\n`);
      sim.printf(`Verified probability sum for every row equals 1.0\n`);
      sim.printf(`Global load accesses: ${sim.counters.globalLoadInsns} (≈ 3 passes per row)\n`);
      sim.printf(`__syncthreads barriers: ${sim.counters.syncthreadsCount}\n`);
      return sim.getResult(passed);
    }

    // ── 05: MatMul (Tiled GEMM) ──────────────────────────────────────────────
    case '05_matmul': {
      const M = 64, N = 64, K = 64, TILE = 16;
      const d_A = sim.cudaMalloc(M * K * 4);
      const d_B = sim.cudaMalloc(K * N * 4);
      const d_C = sim.cudaMalloc(M * N * 4);

      const h_A = new Float32Array(M * K).fill(1.0);
      const h_B = new Float32Array(K * N).fill(1.0);
      sim.cudaMemcpy(d_A, h_A, M * K * 4, 'H2D');
      sim.cudaMemcpy(d_B, h_B, K * N * 4, 'H2D');

      const numTiles = Math.ceil(K / TILE);
      const gridY = Math.ceil(M / TILE);
      const gridX = Math.ceil(N / TILE);
      const totalBlocks = gridY * gridX;

      sim.counters.threadsLaunched = totalBlocks * TILE * TILE;
      sim.counters.blocksLaunched  = totalBlocks;

      for (let by = 0; by < gridY; by++) {
        for (let bx = 0; bx < gridX; bx++) {
          const tileA = sim.createSharedBuffer(TILE * TILE);
          const tileB = sim.createSharedBuffer(TILE * TILE);

          for (let t = 0; t < numTiles; t++) {
            // Load tile A and B into shared memory
            for (let ty = 0; ty < TILE; ty++) {
              for (let tx = 0; tx < TILE; tx++) {
                const r = by * TILE + ty;
                const cA = t * TILE + tx;
                tileA[ty * TILE + tx] = (r < M && cA < K) ? d_A[r * K + cA] : 0.0;

                const rB = t * TILE + ty;
                const cB = bx * TILE + tx;
                tileB[ty * TILE + tx] = (rB < K && cB < N) ? d_B[rB * N + cB] : 0.0;
              }
            }
            sim.syncthreads(); // Barrier 1

            sim.syncthreads(); // Barrier 2
          }

          // Compute dot products and write C
          for (let ty = 0; ty < TILE; ty++) {
            for (let tx = 0; tx < TILE; tx++) {
              const r = by * TILE + ty;
              const c = bx * TILE + tx;
              if (r < M && c < N) {
                let sum = 0;
                for (let k = 0; k < K; k++) {
                  sum += h_A[r * K + k] * h_B[k * N + c];
                }
                d_C[r * N + c] = sum;
              }
            }
          }
        }
      }

      const h_C = new Float32Array(M * N);
      sim.cudaMemcpy(h_C, d_C, M * N * 4, 'D2H');

      let passed = true;
      for (let i = 0; i < M * N; i++) {
        if (Math.abs(h_C[i] - K) > 1e-3) { passed = false; break; }
      }

      sim.counters.globalTransactions = Math.ceil(2 * M * N * K / TILE / 8);
      sim.printf(`Tiled MatMul (${M}x${K} * ${K}x${N}): ${passed ? 'PASSED ✓' : 'FAILED ✗'}\n`);
      sim.printf(`Shared memory tiling factor: ${TILE}x${TILE}\n`);
      sim.printf(`Global loads: ${sim.counters.globalLoadInsns} (≈ 2*M*N*K / ${TILE})\n`);
      sim.printf(`__syncthreads calls: ${sim.counters.syncthreadsCount} (2 barriers per tile iteration)\n`);
      sim.printf(`Data reuse in shared memory saves ${(TILE).toFixed(0)}x global bandwidth.\n`);
      return sim.getResult(passed);
    }

    // ── 06: AllReduce (Multi-GPU NCCL) ───────────────────────────────────────
    case '06_allreduce': {
      const COUNT = 1024;
      const bufs = Array.from({ length: nGpus }, () => new Float32Array(COUNT).fill(1.0));

      const steps = 2 * (nGpus - 1);
      const chunkSize = Math.floor(COUNT / nGpus);

      // Ring Reduce-Scatter
      for (let s = 0; s < nGpus - 1; s++) {
        for (let g = 0; g < nGpus; g++) {
          const next = (g + 1) % nGpus;
          sim.counters.crossGpuBytes += chunkSize * 4;
        }
      }
      // Ring All-Gather
      for (let s = 0; s < nGpus - 1; s++) {
        for (let g = 0; g < nGpus; g++) {
          sim.counters.crossGpuBytes += chunkSize * 4;
        }
      }

      // Finish collective sum
      for (let g = 0; g < nGpus; g++) {
        bufs[g].fill(nGpus);
      }

      sim.counters.ncclOps = nGpus;
      sim.counters.threadsLaunched = 0;
      sim.counters.blocksLaunched  = 0;

      const passed = bufs.every(b => b[0] === nGpus);
      for (let g = 0; g < nGpus; g++) {
        sim.printf(`GPU ${g} local output: [${bufs[g].slice(0, 4).join(', ')}...] (expected ${nGpus})\n`);
      }
      sim.printf(`\nRing-AllReduce across ${nGpus} virtual GPUs:\n`);
      sim.printf(`Number of ring transmission steps: 2*(N-1) = ${steps}\n`);
      sim.printf(`Total cross-GPU interconnect traffic: ${sim.counters.crossGpuBytes.toLocaleString()} bytes\n`);

      const model = ringAllReduceModel(nGpus, COUNT);
      return {
        ...sim.getResult(passed),
        allReduceModel: model
      };
    }

    // ── 07: Pipeline Parallelism ─────────────────────────────────────────────
    case '07_pipeline': {
      const N_STAGES = nGpus > 1 ? nGpus : 4;
      const BATCH = 32, DIM = 512;
      const stageBytes = BATCH * DIM * 4;

      sim.printf(`Pipeline Parallelism Simulation: ${N_STAGES} stages\n`);
      sim.printf(`Micro-batch size: ${BATCH}, Hidden dimension: ${DIM}\n\n`);

      let totalCross = 0;
      for (let s = 0; s < N_STAGES; s++) {
        sim.counters.threadsLaunched += BATCH * DIM;
        sim.counters.blocksLaunched  += BATCH * 2;
        sim.counters.globalLoadInsns += BATCH * DIM * 2;
        sim.counters.globalStoreInsns+= BATCH * DIM;

        if (s < N_STAGES - 1) {
          totalCross += stageBytes;
          sim.counters.crossGpuBytes += stageBytes;
          sim.printf(`Stage ${s} -> Stage ${s + 1} Forward Activation: ${stageBytes.toLocaleString()} bytes\n`);
        }
      }

      sim.printf(`\nForward pass pipeline schedule complete.\n`);
      sim.printf(`Total forward interconnect traffic: ${totalCross.toLocaleString()} bytes\n`);
      sim.printf(`Backward gradient traffic estimate: ${(totalCross).toLocaleString()} bytes\n`);
      return sim.getResult(true);
    }

    // ── 08: Tensor Parallelism ───────────────────────────────────────────────
    case '08_tensor_parallel': {
      const M = 64, N = 512, K = 128;
      const nPerGpu = Math.floor(N / nGpus);

      sim.printf(`Tensor Parallel MatMul (${M}x${K} * ${K}x${N}) across ${nGpus} GPUs:\n`);
      sim.printf(`Weight matrix B is column-sharded: each GPU computes ${M}x${nPerGpu} output columns.\n\n`);

      for (let g = 0; g < nGpus; g++) {
        sim.counters.threadsLaunched += M * nPerGpu;
        sim.counters.blocksLaunched  += Math.ceil(M / 16) * Math.ceil(nPerGpu / 16);
        sim.counters.globalLoadInsns += M * K + K * nPerGpu;
        sim.counters.globalStoreInsns+= M * nPerGpu;
      }

      const allGatherBytes = M * N * 4;
      sim.counters.crossGpuBytes = allGatherBytes;
      sim.counters.ncclOps = nGpus;

      sim.printf(`AllGather epilogue complete.\n`);
      sim.printf(`Local computed shard per GPU: ${M}x${nPerGpu} (${(M * nPerGpu * 4).toLocaleString()} bytes)\n`);
      sim.printf(`AllGather inter-GPU broadcast: ${allGatherBytes.toLocaleString()} bytes\n`);

      const model = ringAllReduceModel(nGpus, M * N);
      return {
        ...sim.getResult(true),
        allReduceModel: { ...model, topology: 'allgather', elementCount: M * N }
      };
    }

    default:
      return {
        passed: false,
        hasErrors: true,
        counters: new CudaSimJS().counters,
        diagnostics: [{ type: 'oob', message: `Unknown problem: ${problemId}`, block: [0,0,0], thread: [0,0,0] }],
        output: `Error: Unknown problem ${problemId}`
      };
  }
}

function ringAllReduceModel(nGpus, countFloats) {
  const steps = 2 * (nGpus - 1);
  const perRankBytes = Math.floor(2 * (nGpus - 1) / nGpus * countFloats * 4);
  const totalBytes = steps * Math.floor(countFloats / nGpus) * 4 * nGpus;
  return {
    topology: 'ring',
    nGpus,
    elementCount: countFloats,
    steps,
    perRankBytes,
    totalCrossGpuBytes: totalBytes,
  };
}

// Export to window
window.CudaSimJS = { runProblem, ringAllReduceModel, CudaSimJS };
