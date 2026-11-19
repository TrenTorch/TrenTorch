/**
 * cuda-runtime.js — Complete GPU Simulation Runtime
 *
 * A browser-based CUDA GPU simulator that executes transpiled CUDA kernels
 * in JavaScript. Provides accurate thread scheduling, memory hierarchy,
 * atomic operations, warp-level primitives, multi-GPU support, and
 * performance counter tracking.
 *
 * Exports: window.CudaRuntime
 */
(function () {
  'use strict';
  function safeRequire(rel) {
    if (typeof require !== 'undefined') {
      try {
        const path = require('path');
        return require(path.join(__dirname, rel));
      } catch (e) {
        try { return require(rel); } catch (e2) { return null; }
      }
    }
    return null;
  }
  const FP16 = safeRequire('fp16-bf16.js') || (typeof window !== 'undefined' ? window.GpuboxFP16 : (typeof globalThis !== 'undefined' ? globalThis.GpuboxFP16 : {}));
  const RaceDetectorModule = safeRequire('race-detector.js') || (typeof window !== 'undefined' ? window.GpuboxRaceDetector : (typeof globalThis !== 'undefined' ? globalThis.GpuboxRaceDetector : {}));
  const SparseMemModule = safeRequire('sparse-memory.js') || (typeof window !== 'undefined' ? window.GpuboxSparseMemory : (typeof globalThis !== 'undefined' ? globalThis.GpuboxSparseMemory : {}));
  const TopologyModule = safeRequire('topology-model.js') || (typeof window !== 'undefined' ? window.GpuboxTopology : (typeof globalThis !== 'undefined' ? globalThis.GpuboxTopology : {}));
  const DesyncModule = safeRequire('desync-detector.js') || (typeof window !== 'undefined' ? window.GpuboxDesyncDetector : (typeof globalThis !== 'undefined' ? globalThis.GpuboxDesyncDetector : {}));


  // ═══════════════════════════════════════════════════════════════════════════
  // Constants
  // ═══════════════════════════════════════════════════════════════════════════

  const WARP_SIZE = 32;
  const SHARED_MEM_BANKS = 32;
  const SECTOR_SIZE_BYTES = 32;
  const POISON_VALUE = 0xDEADBEEF;

  const CUDA_MEMCPY_H2D = 'H2D';
  const CUDA_MEMCPY_D2H = 'D2H';
  const CUDA_MEMCPY_D2D = 'D2D';
  const CUDA_MEMCPY_H2H = 'H2H';

  // CUDA math constants
  const CUDA_INFINITY = Infinity;
  const CUDA_NAN = NaN;
  const CUDA_FLT_MAX = 3.4028235e+38;
  const CUDA_FLT_MIN = 1.1754944e-38;
  const CUDA_FLT_EPSILON = 1.1920929e-7;
  const CUDA_M_PI = Math.PI;
  const CUDA_M_PI_2 = Math.PI / 2;
  const CUDA_M_SQRT2 = Math.SQRT2;

  // ═══════════════════════════════════════════════════════════════════════════
  // Dim3 helper
  // ═══════════════════════════════════════════════════════════════════════════

  /** Normalize a grid/block dimension to {x, y, z}. Accepts number, [x,y,z], or object. */
  function dim3(v) {
    const toDim = (n) => {
      if (n === undefined) return 1;
      const num = Number(n);
      return Number.isNaN(num) ? 1 : Math.floor(num);
    };
    if (typeof v === 'number') // return math context
    return {
                x: toDim(v), y: 1, z: 1 };
    if (Array.isArray(v)) return { x: toDim(v[0]), y: toDim(v[1]), z: toDim(v[2]) };
    if (v && typeof v === 'object') return { x: toDim(v.x), y: toDim(v.y), z: toDim(v.z) };
    return { x: 1, y: 1, z: 1 };
  }

  /** Total number of elements in a dim3 */
  function dim3Volume(d) {
    return d.x * d.y * d.z;
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // SimCounters — performance counter tracking
  // ═══════════════════════════════════════════════════════════════════════════

  class SimCounters {
    constructor(gpuProfile) {
      this._gpuProfile = gpuProfile || {};
      this.reset();
    }

    reset() {
      // Launch counters
      this.threadsLaunched = 0;
      this.blocksLaunched = 0;

      // Global memory
      this.globalLoads = 0;
      this.globalStores = 0;
      this.globalLoadBytes = 0;
      this.globalStoreBytes = 0;
      this.globalTransactions = 0;

      // Shared memory
      this.sharedLoads = 0;
      this.sharedStores = 0;
      this.sharedLoadBytes = 0;
      this.sharedStoreBytes = 0;
      this.bankConflicts = 0;
      this.bankAccesses = new Array(32).fill(0);   // distinct words touched per bank, over all warp accesses
      this.bankReplays = new Array(32).fill(0);    // extra serialised passes caused in each bank

      // Synchronization
      this.syncthreadsCount = 0;

      // Branch divergence
      this.divergentBranches = 0;
      this.branchEvents = 0;
      this.idealGlobalTransactions = 0;
      this._branchOutcomes = new Map();
      this._branchOcc = new Map();
      this._sharedWindows = new Map();
      this._sharedSeq = new Map();

      // Atomics
      this.atomicOps = 0;
      this.atomicMaxContention = 0;

      // Memory copy
      this.memcpyH2DBytes = 0;
      this.memcpyD2HBytes = 0;

      // Multi-GPU / NCCL
      this.crossGpuBytes = 0;
      this.ncclOps = 0;

      // Instruction counters for utilization
      this.flopCount = 0;

      // Warp-level tracking: per-warp address sets for coalescing analysis
      this._warpGlobalAccesses = [];
      this._warpAccessWindows = new Map();
      this._threadAccessSeq = new Map();
      this._activeWarpId = undefined;
      this._activeThreadId = undefined;
      // Per-warp shared bank tracking
      this._warpSharedBanks = [];
      // Atomic contention tracking per kernel launch
      this._atomicContentionMap = new Map();
    }

    /** Set active thread and warp context for SIMT analysis */
    setActiveContext(warpId, threadId) {
      this._activeWarpId = warpId;
      this._activeThreadId = threadId;
    }

    /** Clear active thread context */
    clearActiveContext() {
      this._activeWarpId = undefined;
      this._activeThreadId = undefined;
    }

    /** Record a global memory load */
    recordGlobalLoad(elementBytes, byteAddr) {
      this.globalLoads++;
      this.globalLoadBytes += (elementBytes || 4);
      this._recordGlobalAccess(byteAddr, elementBytes);
    }

    /** One 16-byte vector load: a single instruction touching four consecutive words */
    recordGlobalLoadVec(byteAddr) {
      this.globalLoads++;
      this.globalLoadBytes += 16;
      this._recordGlobalAccess(byteAddr, 4, [byteAddr + 4, byteAddr + 8, byteAddr + 12]);
    }

    recordGlobalStoreVec(byteAddr) {
      this.globalStores++;
      this.globalStoreBytes += 16;
      this._recordGlobalAccess(byteAddr, 4, [byteAddr + 4, byteAddr + 8, byteAddr + 12]);
    }

    /** Record a global memory store */
    recordGlobalStore(elementBytes, byteAddr) {
      this.globalStores++;
      this.globalStoreBytes += (elementBytes || 4);
      this._recordGlobalAccess(byteAddr, elementBytes);
    }

    /** Record internal address access for 32-byte transaction coalescing */
    _recordGlobalAccess(byteAddr, elementBytes, extraAddrs) {
      const addr = byteAddr !== undefined ? byteAddr : 0;
      if (this._activeWarpId !== undefined && this._activeThreadId !== undefined) {
        const threadKey = this._activeWarpId + ':' + this._activeThreadId;
        const seq = this._threadAccessSeq.get(threadKey) || 0;
        this._threadAccessSeq.set(threadKey, seq + 1);
        const windowKey = this._activeWarpId + ':' + seq;
        let window = this._warpAccessWindows.get(windowKey);
        if (!window) {
          window = [];
          window.eb = elementBytes || 4;
          this._warpAccessWindows.set(windowKey, window);
        }
        window.push(addr);
        if (extraAddrs) for (let e = 0; e < extraAddrs.length; e++) window.push(extraAddrs[e]);
      } else {
        this.globalTransactions++;
      }
    }

    /** Flush all pending warp global access windows and compute transaction counts */
    flushWarpGlobalAccesses() {
      if (!this._warpAccessWindows || this._warpAccessWindows.size === 0) return;
      for (const [_, addresses] of this._warpAccessWindows) {
        if (!addresses || addresses.length === 0) continue;
        const sectors = new Set();
        for (let i = 0; i < addresses.length; i++) {
          sectors.add(Math.floor(addresses[i] / SECTOR_SIZE_BYTES));
        }
        this.globalTransactions += sectors.size;
        this.idealGlobalTransactions += Math.max(1, Math.ceil(addresses.length * (addresses.eb || 4) / SECTOR_SIZE_BYTES));
      }
      this._warpAccessWindows.clear();
      this._threadAccessSeq.clear();
      this.flushBranches();
    }

    /** Record one evaluation of a source-level branch condition by the active lane */
    recordBranch(site, taken) {
      const w = this._activeWarpId === undefined ? 0 : this._activeWarpId;
      const t = this._activeThreadId === undefined ? 0 : this._activeThreadId;
      const ok = w + ':' + t + ':' + site;
      const occ = this._branchOcc.get(ok) || 0;
      this._branchOcc.set(ok, occ + 1);
      const key = w + ':' + site + ':' + occ;
      this._branchOutcomes.set(key, (this._branchOutcomes.get(key) || 0) | (taken ? 1 : 2));
    }

    /** A warp-level branch event is divergent if lanes disagreed on the outcome */
    flushBranches() {
      for (const bits of this._branchOutcomes.values()) {
        this.branchEvents++;
        if (bits === 3) this.divergentBranches++;
      }
      this._branchOutcomes.clear();
      this._branchOcc.clear();
    }

    /** Statically estimated FLOPs, charged per executed statement */
    recordFlops(n) { this.flopCount += n; }

    /** Record branch divergence */
    recordDivergentBranch() {
      this.divergentBranches++;
    }

    /** Record a shared memory load */
    recordSharedLoad(byteAddr) {
      this.sharedLoads++;
      this.sharedLoadBytes += 4;
      this._recordSharedAccess(byteAddr);
    }

    _recordSharedAccess(byteAddr) {
      const word = Math.floor(byteAddr / 4);
      const w = this._activeWarpId === undefined ? 0 : this._activeWarpId;
      const t = this._activeThreadId === undefined ? 0 : this._activeThreadId;
      const tk = w + ':' + t;
      const seq = this._sharedSeq.get(tk) || 0;
      this._sharedSeq.set(tk, seq + 1);
      const wk = w + ':' + seq;
      let win = this._sharedWindows.get(wk);
      if (!win) { win = new Set(); this._sharedWindows.set(wk, win); }
      win.add(word);
    }

    /** Record a shared memory store */
    recordSharedStore(byteAddr) {
      this.sharedStores++;
      this.sharedStoreBytes += 4;
      this._recordSharedAccess(byteAddr);
    }

    /** Flush per-warp shared bank accesses and count conflicts */
    flushSharedBankAccesses() {
      // A warp access replays once per extra distinct word in its busiest bank.
      // Same-word accesses are broadcasts and are not conflicts.
      for (const words of this._sharedWindows.values()) {
        if (words.size === 1) { for (const wd of words) this.bankAccesses[wd % SHARED_MEM_BANKS]++; continue; }
        if (words.size < 1) continue;
        const perBank = new Int32Array(SHARED_MEM_BANKS);
        for (const wd of words) perBank[wd % SHARED_MEM_BANKS]++;
        let worst = 0;
        for (let b = 0; b < SHARED_MEM_BANKS; b++) {
          this.bankAccesses[b] += perBank[b];
          if (perBank[b] > worst) worst = perBank[b];
        }
        if (worst > 1) {
          this.bankConflicts += worst - 1;
          for (let b = 0; b < SHARED_MEM_BANKS; b++) if (perBank[b] > 1) this.bankReplays[b] += perBank[b] - 1;
        }
      }
      this._sharedWindows.clear();
      this._sharedSeq.clear();
      this._warpSharedBanks = [];
    }

    /** Record a warp's global memory access for transaction/coalescing analysis */
    recordWarpGlobalAccess(byteAddresses) {
      // Count 32-byte sectors touched
      const sectors = new Set();
      for (let i = 0; i < byteAddresses.length; i++) {
        sectors.add(Math.floor(byteAddresses[i] / SECTOR_SIZE_BYTES));
      }
      this.globalTransactions += sectors.size;
    }

    /** Record an atomic operation and track contention */
    recordAtomic(allocId, index) {
      this.atomicOps++;
      const key = allocId + ':' + index;
      const prev = this._atomicContentionMap.get(key) || 0;
      const next = prev + 1;
      this._atomicContentionMap.set(key, next);
      if (next > this.atomicMaxContention) {
        this.atomicMaxContention = next;
      }
    }

    /** Record a floating-point operation */
    recordFlop(count) {
      this.flopCount += (count || 1);
    }

    // ── Derived metrics ──

    /** Estimated cycles based on GPU profile latencies */
    get estimatedCycles() {
      const prof = this._gpuProfile;
      const globalLatency = prof.globalMemLatencyCycles || 400;
      const sharedLatency = prof.sharedMemLatencyCycles || 20;
      const atomicLatency = prof.atomicLatencyCycles || 50;
      const syncLatency = prof.syncLatencyCycles || 5;
      const flopLatency = prof.flopLatencyCycles || 1;

      return (this.globalLoads + this.globalStores) * globalLatency +
        (this.sharedLoads + this.sharedStores) * sharedLatency +
        this.atomicOps * atomicLatency +
        this.syncthreadsCount * syncLatency +
        this.flopCount * flopLatency;
    }

    /** Estimated wall-clock time in milliseconds */
    get estimatedTimeMs() {
      const clockHz = (this._gpuProfile.clockSpeedMHz || 1500) * 1e6;
      return (this.estimatedCycles / clockHz) * 1000;
    }

    /** Compute utilization: FLOPs / peak FLOPs over the estimated time */
    get computeUtilization() {
      const peakGFLOPS = this._gpuProfile.peakTFLOPS
        ? this._gpuProfile.peakTFLOPS * 1000
        : (this._gpuProfile.peakGFLOPS || 10000);
      const timeSec = this.estimatedTimeMs / 1000;
      if (timeSec === 0) return 0;
      const actualGFLOPS = (this.flopCount / 1e9) / timeSec;
      return Math.min(actualGFLOPS / peakGFLOPS, 1.0);
    }

    /** Memory bandwidth utilization */
    get memoryUtilization() {
      const peakBWGBs = this._gpuProfile.memBandwidthGBs || 900;
      const totalBytes = this.globalLoadBytes + this.globalStoreBytes;
      const timeSec = this.estimatedTimeMs / 1000;
      if (timeSec === 0) return 0;
      const actualGBs = (totalBytes / 1e9) / timeSec;
      return Math.min(actualGBs / peakBWGBs, 1.0);
    }

    /** Occupancy: threads / maxThreadsPerSM */
    get occupancy() {
      const maxThreadsPerSM = this._gpuProfile.maxThreadsPerSM || 2048;
      const smCount = this._gpuProfile.smCount || 80;
      if (smCount === 0) return 0;
      return Math.min(this.threadsLaunched / (maxThreadsPerSM * smCount), 1.0);
    }

    get totalBytesRead() { return this.globalLoadBytes; }
    get totalBytesWritten() { return this.globalStoreBytes; }
    get coalescedTransactions() { return this.idealGlobalTransactions; }
    get dramReadBytes() { return this.globalLoadBytes; }
    get dramWriteBytes() { return this.globalStoreBytes; }

    toJSON() {
      const res = {
        threadsLaunched: this.threadsLaunched,
        blocksLaunched: this.blocksLaunched,
        globalLoads: this.globalLoads,
        globalStores: this.globalStores,
        globalLoadBytes: this.globalLoadBytes,
        globalStoreBytes: this.globalStoreBytes,
        totalBytesRead: this.globalLoadBytes,
        totalBytesWritten: this.globalStoreBytes,
        globalTransactions: this.globalTransactions,
        coalescedTransactions: this.idealGlobalTransactions,
        idealGlobalTransactions: this.idealGlobalTransactions,
        coalescingEfficiency: this.globalTransactions ? Math.min(1, this.idealGlobalTransactions / this.globalTransactions) : 1,
        branchEvents: this.branchEvents,
        dramReadBytes: this.globalLoadBytes,
        dramWriteBytes: this.globalStoreBytes,
        sharedLoads: this.sharedLoads,
        sharedStores: this.sharedStores,
        sharedLoadBytes: this.sharedLoadBytes,
        sharedStoreBytes: this.sharedStoreBytes,
        bankConflicts: this.bankConflicts,
        bankAccesses: this.bankAccesses.slice(),
        bankReplays: this.bankReplays.slice(),
        syncthreadsCount: this.syncthreadsCount,
        divergentBranches: this.divergentBranches,
        atomicOps: this.atomicOps,
        atomicMaxContention: this.atomicMaxContention,
        memcpyH2DBytes: this.memcpyH2DBytes,
        memcpyD2HBytes: this.memcpyD2HBytes,
        crossGpuBytes: this.crossGpuBytes,
        ncclOps: this.ncclOps,
        flopCount: this.flopCount,
        estimatedCycles: this.estimatedCycles,
        estimatedTimeMs: this.estimatedTimeMs,
        computeUtilization: this.computeUtilization,
        memoryUtilization: this.memoryUtilization,
        occupancy: this.occupancy
      };
      if (this.perDevice) {
        res.perDevice = this.perDevice;
      }
      return res;
    }
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // DevicePointer — typed view into the global memory arena
  // ═══════════════════════════════════════════════════════════════════════════

  let _nextAllocId = 1;

  class DevicePointer {
    /**
     * @param {ArrayBuffer} buffer   – Backing ArrayBuffer
     * @param {number}      offset   – Element offset within the typed view
     * @param {number}      elementSize – Bytes per element (1, 2, 4)
     * @param {number}      allocId  – Unique allocation identifier
     * @param {SimCounters} counters – Runtime counters for tracking
     * @param {number}      allocLength – Total elements in this allocation
     */
    constructor(buffer, offset, elementSize, allocId, counters, allocLength) {
      this._buffer = buffer;
      this._offset = offset;
      this._elementSize = elementSize;
      this._allocId = allocId;
      this._counters = counters;
      this._allocLength = allocLength;

      // Build the appropriate typed view
      if (elementSize === 4) {
        this._f32 = new Float32Array(buffer);
        this._i32 = new Int32Array(buffer);
      }
      this._u8 = new Uint8Array(buffer);

      return new Proxy(this, {
        get(target, prop, receiver) {
          if (typeof prop === 'string' && /^\d+$/.test(prop)) {
            return target.get(parseInt(prop, 10));
          }
          return Reflect.get(target, prop, receiver);
        },
        set(target, prop, value, receiver) {
          if (typeof prop === 'string' && /^\d+$/.test(prop)) {
            target.set(parseInt(prop, 10), value);
            return true;
          }
          return Reflect.set(target, prop, value, receiver);
        }
      });
    }

    /** Read element at logical index (relative to this pointer's offset) */
    get(index) {
      if (this._sparseBuffer) {
        if (this._isFreed) throw new Error('cudaErrorIllegalAddress: use-after-free detected');
        const absIdx = this._offset + index;
        if (this._counters) this._counters.recordGlobalLoad(this._elementSize, absIdx * this._elementSize);
        return this._sparseBuffer.get(absIdx);
      }
      if (this._isFreed) {
        throw new Error('cudaErrorIllegalAddress: access to freed device pointer');
      }
      const absIdx = this._offset + index;
      if (absIdx < 0 || absIdx >= this._allocLength) {
        throw new RangeError(
          'DevicePointer OOB read: index ' + absIdx + ' (alloc size ' + this._allocLength + ')'
        );
      }
      if (this._counters) {
        this._counters.recordGlobalLoad(this._elementSize, absIdx * this._elementSize);
      }
      if (this._elementSize === 4) {
        return this._f32[absIdx];
      }
      return this._u8[absIdx];
    }

    /** Write element at logical index */
    set(index, value) {
      if (this._sparseBuffer) {
        if (this._isFreed) throw new Error('cudaErrorIllegalAddress: use-after-free detected');
        const absIdx = this._offset + index;
        if (this._counters) this._counters.recordGlobalStore(this._elementSize, absIdx * this._elementSize);
        this._sparseBuffer.set(absIdx, value);
        return;
      }
      if (this._isFreed) {
        throw new Error('cudaErrorIllegalAddress: access to freed device pointer');
      }
      const absIdx = this._offset + index;
      if (absIdx < 0 || absIdx >= this._allocLength) {
        throw new RangeError(
          'DevicePointer OOB write: index ' + absIdx + ' (alloc size ' + this._allocLength + ')'
        );
      }
      if (this._counters) {
        this._counters.recordGlobalStore(this._elementSize, absIdx * this._elementSize);
      }
      if (this._elementSize === 4) {
        this._f32[absIdx] = value;
      } else {
        this._u8[absIdx] = value;
      }
    }

    /** float4 load of elements [4v, 4v+3]; the address must be 16-byte aligned */
    getVec4(v, base) {
      const a = this._offset + (base || 0) + 4 * v;
      if (this._isFreed) throw new Error('cudaErrorIllegalAddress: access to freed device pointer');
      if (a < 0 || a + 3 >= this._allocLength) throw new RangeError('DevicePointer OOB read: float4 at element ' + a + ' (alloc size ' + this._allocLength + ')');
      if ((a * this._elementSize) % 16 !== 0) throw new Error('cudaErrorMisalignedAddress: float4 access at byte ' + a * this._elementSize + ' is not 16-byte aligned');
      if (this._counters) this._counters.recordGlobalLoadVec(a * this._elementSize);
      const f = this._f32;
      return { x: f[a], y: f[a + 1], z: f[a + 2], w: f[a + 3] };
    }

    setVec4(v, o, base) {
      const a = this._offset + (base || 0) + 4 * v;
      if (this._isFreed) throw new Error('cudaErrorIllegalAddress: access to freed device pointer');
      if (a < 0 || a + 3 >= this._allocLength) throw new RangeError('DevicePointer OOB write: float4 at element ' + a + ' (alloc size ' + this._allocLength + ')');
      if ((a * this._elementSize) % 16 !== 0) throw new Error('cudaErrorMisalignedAddress: float4 access at byte ' + a * this._elementSize + ' is not 16-byte aligned');
      if (this._counters) this._counters.recordGlobalStoreVec(a * this._elementSize);
      const f = this._f32;
      f[a] = o.x; f[a + 1] = o.y; f[a + 2] = o.z; f[a + 3] = o.w;
    }

    /** Raw read (bypasses counter tracking) – used for atomics, memcpy */
    _rawGet(index) {
      if (this._sparseBuffer) return this._sparseBuffer.get(this._offset + index);
      const absIdx = this._offset + index;
      if (this._elementSize === 4) return this._f32[absIdx];
      return this._u8[absIdx];
    }

    /** Raw write (bypasses counter tracking) */
    _rawSet(index, value) {
      if (this._sparseBuffer) { this._sparseBuffer.set(this._offset + index, value); return; }
      const absIdx = this._offset + index;
      if (this._elementSize === 4) this._f32[absIdx] = value;
      else this._u8[absIdx] = value;
    }

    /** Raw i32 read at absolute index (for atomics) */
    _rawGetI32(index) {
      return this._i32[this._offset + index];
    }

    /** Raw i32 write at absolute index (for atomics) */
    _rawSetI32(index, value) {
      this._i32[this._offset + index] = value;
    }

    /** Pointer arithmetic: advance by n elements */
    add(n) {
      return new DevicePointer(
        this._buffer, this._offset + n, this._elementSize,
        this._allocId, this._counters, this._allocLength
      );
    }

    /** Pointer arithmetic: retreat by n elements */
    sub(n) {
      return new DevicePointer(
        this._buffer, this._offset - n, this._elementSize,
        this._allocId, this._counters, this._allocLength
      );
    }

    /** Reinterpret as float pointer (4 bytes per element) */
    castFloat() {
      const byteOffset = this._offset * this._elementSize;
      const newOffset = Math.floor(byteOffset / 4);
      const newLength = Math.floor((this._allocLength * this._elementSize) / 4);
      return new DevicePointer(
        this._buffer, newOffset, 4, this._allocId, this._counters, newLength
      );
    }

    /** Reinterpret as int pointer (4 bytes per element) */
    castInt() {
      return this.castFloat(); // same layout, i32 view is always available
    }

    /** Read a float4 (4 floats) at float4-index (16-byte aligned) */
    getFloat4(index) {
      const base = (index || 0) * 4;
      return {
        x: this.get(base),
        y: this.get(base + 1),
        z: this.get(base + 2),
        w: this.get(base + 3),
      };
    }

    /** Write a float4 at float4-index */
    setFloat4(index, v) {
      const base = (index || 0) * 4;
      const val = v || {};
      this.set(base, val.x !== undefined ? val.x : 0);
      this.set(base + 1, val.y !== undefined ? val.y : 0);
      this.set(base + 2, val.z !== undefined ? val.z : 0);
      this.set(base + 3, val.w !== undefined ? val.w : 0);
    }

    /** Read a float2 (2 floats) */
    getFloat2(index) {
      const base = (index || 0) * 2;
      return { x: this.get(base), y: this.get(base + 1) };
    }

    /** Write a float2 */
    setFloat2(index, v) {
      const base = (index || 0) * 2;
      const val = v || {};
      this.set(base, val.x !== undefined ? val.x : 0);
      this.set(base + 1, val.y !== undefined ? val.y : 0);
    }

    /** Read an int4 */
    getInt4(index) {
      return this.getFloat4(index);
    }

    /** Write an int4 */
    setInt4(index, v) {
      this.setFloat4(index, v);
    }

    /** Copy count elements from device to a new host Float32Array */
    toFloat32Array(count) {
      const result = new Float32Array(count);
      const f32 = new Float32Array(this._buffer);
      for (let i = 0; i < count; i++) {
        result[i] = f32[this._offset + i];
      }
      return result;
    }

    /** Copy a host Float32Array into device memory starting at this pointer */
    fromFloat32Array(arr) {
      const f32 = new Float32Array(this._buffer);
      for (let i = 0; i < arr.length; i++) {
        f32[this._offset + i] = arr[i];
      }
    }

    /** Byte address of element at index (for coalescing analysis) */
    _byteAddress(index) {
      return (this._offset + index) * this._elementSize;
    }

    /** Returns the underlying ArrayBuffer */
    get buffer() { return this._buffer; }

    /** Returns the element offset */
    get offset() { return this._offset; }

    /** Returns the element size in bytes */
    get elementSize() { return this._elementSize; }

    /** Returns the allocation ID */
    get allocId() { return this._allocId; }
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // SimMemory — global device memory arena
  // ═══════════════════════════════════════════════════════════════════════════

  class SimMemory {
    constructor(counters, deviceId = 0, profile) {
      this._counters = counters;
      this._deviceId = deviceId;
      this._profile = profile || (typeof GPU_PROFILES !== 'undefined' ? GPU_PROFILES.getProfile('A100') : { globalMemoryGB: 80 });
      this._capacityBytes = (this._profile.globalMemoryGB || 80) * 1024 * 1024 * 1024;
      this._allocatedBytes = 0;
      /** @type {Map<number, {buffer: ArrayBuffer|null, sparse: any, sizeBytes: number}>} */
      this._allocations = new Map();
    }


    /**
     * Allocate device memory.
     * @param {number} sizeBytes – Number of bytes to allocate
     * @returns {DevicePointer} pointer to the allocation (float32 view by default)
     */
    cudaMalloc(sizeBytes) {
      if (typeof sizeBytes !== 'number' || sizeBytes < 0) {
        throw new Error('cudaErrorMemoryAllocation: invalid allocation size ' + sizeBytes);
      }
      // Round up to 4-byte alignment
      const aligned = Math.max(0, Math.ceil(sizeBytes / 4) * 4);
      if (this._allocatedBytes + aligned > this._capacityBytes) {
        throw new Error('cudaErrorMemoryAllocation: out of memory on device ' + this._deviceId + ' (requested ' + aligned + ' bytes, allocated ' + this._allocatedBytes + ' bytes, capacity ' + this._capacityBytes + ' bytes)');
      }

      const allocId = _nextAllocId++;
      const elementSize = 4;
      const allocLength = aligned / elementSize;
      const maxDirectBytes = 16 * 1024 * 1024; // 16 MB

      if (aligned > maxDirectBytes) {
        const sparse = new SparseMemModule.SparseVirtualBuffer(aligned, this._deviceId);
        this._allocations.set(allocId, { buffer: null, sparse, sizeBytes: aligned });
        this._allocatedBytes += aligned;
        const ptr = new DevicePointer(null, 0, elementSize, allocId, this._counters, allocLength);
        ptr._sparseBuffer = sparse;
        ptr._deviceId = this._deviceId !== undefined ? this._deviceId : 0;
        return ptr;
      }

      const buffer = new ArrayBuffer(aligned);
      this._allocations.set(allocId, { buffer, sparse: null, sizeBytes: aligned });
      this._allocatedBytes += aligned;

      const ptr = new DevicePointer(buffer, 0, elementSize, allocId, this._counters, allocLength);
      ptr._deviceId = this._deviceId !== undefined ? this._deviceId : 0;
      return ptr;
    }

    /**
     * Free a device allocation.
     * @param {DevicePointer} ptr
     */
    cudaFree(ptr) {
      if (ptr && ptr._allocId !== undefined) {
        if (ptr._isFreed) {
          throw new Error('cudaErrorInvalidValue: double free or invalid pointer in cudaFree');
        }
        const alloc = this._allocations.get(ptr._allocId);
        if (!alloc) {
          throw new Error('cudaErrorInvalidValue: double free or invalid pointer in cudaFree');
        }
        this._allocatedBytes = Math.max(0, this._allocatedBytes - alloc.sizeBytes);
        if (alloc.sparse) {
          alloc.sparse.free();
        }
        this._allocations.delete(ptr._allocId);
        ptr._isFreed = true;
      }
    }

    /**
     * Copy data between host and device.
     * @param {DevicePointer|Float32Array|Int32Array|Uint8Array} dst
     * @param {DevicePointer|Float32Array|Int32Array|Uint8Array} src
     * @param {number} sizeBytes
     * @param {string} kind – 'H2D', 'D2H', 'D2D', 'H2H'
     */
    cudaMemcpy(dst, src, sizeBytes, kind) {
      if (!dst) throw new Error('cudaErrorInvalidValue: null destination pointer in cudaMemcpy');
      if (!src) throw new Error('cudaErrorInvalidValue: null source pointer in cudaMemcpy');
      if (typeof sizeBytes !== 'number' || sizeBytes < 0) {
        throw new Error('cudaErrorInvalidValue: invalid or negative sizeBytes in cudaMemcpy (' + sizeBytes + ')');
      }
      if (!kind || kind === 'DEFAULT' || kind === 'cudaMemcpyDefault' || kind === 0) {
        if (dst instanceof DevicePointer && !(src instanceof DevicePointer)) kind = CUDA_MEMCPY_H2D;
        else if (!(dst instanceof DevicePointer) && src instanceof DevicePointer) kind = CUDA_MEMCPY_D2H;
        else if (dst instanceof DevicePointer && src instanceof DevicePointer) kind = CUDA_MEMCPY_D2D;
        else kind = CUDA_MEMCPY_H2H;
      }
      switch (kind) {
        case CUDA_MEMCPY_H2D: {
          // src is host typed array, dst is DevicePointer
          const dstU8 = new Uint8Array(dst._buffer, dst._offset * dst._elementSize);
          if (ArrayBuffer.isView(src)) {
            const copyLen = Math.min(sizeBytes, src.byteLength);
            const srcU8 = new Uint8Array(src.buffer, src.byteOffset, copyLen);
            dstU8.set(srcU8.subarray(0, copyLen));
          } else if (Array.isArray(src)) {
            const f32 = new Float32Array(src);
            const copyLen = Math.min(sizeBytes, f32.byteLength);
            const srcU8 = new Uint8Array(f32.buffer, 0, copyLen);
            dstU8.set(srcU8);
          } else if (typeof src === 'number') {
            new Float32Array(dst._buffer, dst._offset * dst._elementSize, 1)[0] = src;
          } else if (typeof src === 'string') {
            const nums = src.split(',').map(Number).filter(n => !Number.isNaN(n));
            if (nums.length > 0) {
              const f32 = new Float32Array(nums);
              const copyLen = Math.min(sizeBytes, f32.byteLength);
              const srcU8 = new Uint8Array(f32.buffer, 0, copyLen);
              dstU8.set(srcU8);
            }
          }
          this._counters.memcpyH2DBytes += sizeBytes;
          break;
        }
        case CUDA_MEMCPY_D2H: {
          // src is DevicePointer, dst is host typed array
          const dstLen = dst && dst.byteLength !== undefined ? dst.byteLength : sizeBytes;
          const availableSrcBytes = Math.max(0, (src._buffer ? src._buffer.byteLength : 0) - (src._offset * src._elementSize));
          const copyLen = Math.min(sizeBytes, dstLen, availableSrcBytes);
          const srcU8 = new Uint8Array(src._buffer, src._offset * src._elementSize, copyLen);
          if (ArrayBuffer.isView(dst)) {
            const dstU8 = new Uint8Array(dst.buffer, dst.byteOffset);
            dstU8.set(srcU8.subarray(0, copyLen));
          } else if (Array.isArray(dst)) {
            const f32 = new Float32Array(src._buffer, src._offset * src._elementSize, Math.floor(copyLen / 4));
            for (let i = 0; i < f32.length; i++) dst[i] = f32[i];
          }
          this._counters.memcpyD2HBytes += copyLen;
          break;
        }
        case CUDA_MEMCPY_D2D: {
          // Both are DevicePointers
          const availableSrcBytes = Math.max(0, (src._buffer ? src._buffer.byteLength : 0) - (src._offset * src._elementSize));
          const availableDstBytes = Math.max(0, (dst._buffer ? dst._buffer.byteLength : 0) - (dst._offset * dst._elementSize));
          const copyLen = Math.min(sizeBytes, availableSrcBytes, availableDstBytes);
          const srcU8 = new Uint8Array(src._buffer, src._offset * src._elementSize, copyLen);
          const dstU8 = new Uint8Array(dst._buffer, dst._offset * dst._elementSize);
          dstU8.set(srcU8.subarray(0, copyLen));
          break;
        }
        case CUDA_MEMCPY_H2H: {
          // Both are host typed arrays
          const srcU8 = new Uint8Array(src.buffer, src.byteOffset, sizeBytes);
          const dstU8 = new Uint8Array(dst.buffer, dst.byteOffset);
          dstU8.set(srcU8.subarray(0, sizeBytes));
          break;
        }
        default:
          throw new Error('Unknown cudaMemcpy kind: ' + kind);
      }
    }

    /**
     * Set device memory to a byte value.
     * @param {DevicePointer} ptr
     * @param {number} value – Byte value (0-255)
     * @param {number} sizeBytes
     */
    cudaMemset(ptr, value, sizeBytes) {
      const u8 = new Uint8Array(ptr._buffer, ptr._offset * ptr._elementSize);
      for (let i = 0; i < sizeBytes; i++) {
        u8[i] = value & 0xFF;
      }
    }

    /** Destroy all allocations */
    destroy() {
      this._allocations.clear();
    }
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // SharedMemory — per-block shared memory with bank conflict tracking
  // ═══════════════════════════════════════════════════════════════════════════

  class SharedMemory {
    /**
     * @param {number} sizeBytes – Size in bytes
     * @param {SimCounters} counters
     */
    constructor(sizeBytes, counters) {
      this._sizeBytes = sizeBytes;
      this._counters = counters;
      // Backing store as float32 (most common use)
      const aligned = Math.max(1024, Math.ceil((sizeBytes || 1024) / 4) * 4);
      this._buffer = new ArrayBuffer(aligned);
      this._f32 = new Float32Array(this._buffer);
      this._i32 = new Int32Array(this._buffer);
      this._u8 = new Uint8Array(this._buffer);

      // Static shared arrays map: name -> typed array
      this._staticArrays = new Map();
      this._raceDetector = new RaceDetectorModule.SharedMemoryRaceDetector();
      this._currentCtx = null;

      // Poison-fill to detect uninitialized reads
      this._i32.fill(POISON_VALUE);
      // Track which indices have been written
      this._written = new Uint8Array(this._f32.length);

      return new Proxy(this, {
        get(target, prop, receiver) {
          if (typeof prop === 'string' && /^\d+$/.test(prop)) {
            const idx = parseInt(prop, 10);
            return target.get(idx);
          }
          return Reflect.get(target, prop, receiver);
        },
        set(target, prop, value, receiver) {
          if (typeof prop === 'string' && /^\d+$/.test(prop)) {
            const idx = parseInt(prop, 10);
            target.set(idx, value);
            return true;
          }
          return Reflect.set(target, prop, value, receiver);
        }
      });
    }

    /**
     * Get or create a named static shared array shared across all threads in the block.
     * @param {string} name
     * @param {number} size
     * @param {string} type
     * @returns {Float32Array|Int32Array}
     */
    setActiveContext(ctx) {
      this._currentCtx = ctx;
    }

    getArray(name, size, type = 'float32') {
      if (!this._staticArrays.has(name)) {
        // size 0 = extern __shared__: use the dynamic shared memory the launch asked for
        const count = size || (this._sizeBytes > 0 ? Math.floor(this._sizeBytes / 4) : 256);
        const raw = (type === 'int' || type === 'int32') ? new Int32Array(count) : new Float32Array(count);
        const self = this;
        const proxy = new Proxy(raw, {
          get(target, prop, receiver) {
            if (prop === '__raw') return target;
            if (typeof prop === 'string' && /^\d+$/.test(prop)) {
              const idx = parseInt(prop, 10);
              if (idx < 0 || idx >= target.length) {
                throw new RangeError(`SharedMemory static array OOB read at index ${idx} (size ${target.length})`);
              }
              self._counters.recordSharedLoad(idx * 4);
              if (self._raceDetector && self._currentCtx) self._raceDetector.recordAccess(name, idx, false, self._currentCtx);
              return target[idx];
            }
            return Reflect.get(target, prop, receiver);
          },
          set(target, prop, value, receiver) {
            if (typeof prop === 'string' && /^\d+$/.test(prop)) {
              const idx = parseInt(prop, 10);
              if (idx < 0 || idx >= target.length) {
                throw new RangeError(`SharedMemory static array OOB write at index ${idx} (size ${target.length})`);
              }
              self._counters.recordSharedStore(idx * 4);
              if (self._raceDetector && self._currentCtx) self._raceDetector.recordAccess(name, idx, true, self._currentCtx);
              target[idx] = value;
              return true;
            }
            return Reflect.set(target, prop, value, receiver);
          }
        });
        this._staticArrays.set(name, proxy);
      }
      return this._staticArrays.get(name);
    }

    /**
     * Get or create a 2D static shared array (e.g. As[TILE][TILE]) shared across all threads in the block.
     * @param {string} name
     * @param {number} rows
     * @param {number} cols
     * @param {string} type
     * @returns {Array<Float32Array|Int32Array>}
     */
    get2DArray(name, rows, cols, type = 'float32') {
      if (!this._staticArrays.has(name)) {
        const r = rows || 16;
        const c = cols || 16;
        const grid = [];
        const self = this;
        for (let i = 0; i < r; i++) {
          const rawRow = (type === 'int' || type === 'int32') ? new Int32Array(c) : new Float32Array(c);
          const rowIdx = i;
          const rowProxy = new Proxy(rawRow, {
            get(target, prop, receiver) {
              if (typeof prop === 'string' && /^\d+$/.test(prop)) {
                const colIdx = parseInt(prop, 10);
                self._counters.recordSharedLoad((rowIdx * c + colIdx) * 4);
                if (self._raceDetector && self._currentCtx) self._raceDetector.recordAccess(name, rowIdx * c + colIdx, false, self._currentCtx);
                return target[colIdx];
              }
              return Reflect.get(target, prop, receiver);
            },
            set(target, prop, value, receiver) {
              if (typeof prop === 'string' && /^\d+$/.test(prop)) {
                const colIdx = parseInt(prop, 10);
                self._counters.recordSharedStore((rowIdx * c + colIdx) * 4);
                if (self._raceDetector && self._currentCtx) self._raceDetector.recordAccess(name, rowIdx * c + colIdx, true, self._currentCtx);
                target[colIdx] = value;
                return true;
              }
              return Reflect.set(target, prop, value, receiver);
            }
          });
          grid.push(rowProxy);
        }
        this._staticArrays.set(name, grid);
      }
      return this._staticArrays.get(name);
    }

    /** Read float at index */
    get(index) {
      const maxFloats = Math.floor(this._sizeBytes / 4);
      if (index < 0 || index >= maxFloats) {
        throw new RangeError('SharedMemory OOB read at index ' + index + ' (size ' + maxFloats + ')');
      }
      const byteAddr = index * 4;
      this._counters.recordSharedLoad(byteAddr);
      return this._f32[index];
    }

    /** Write float at index */
    set(index, value) {
      const maxFloats = Math.floor(this._sizeBytes / 4);
      if (index < 0 || index >= maxFloats) {
        throw new RangeError('SharedMemory OOB write at index ' + index + ' (size ' + maxFloats + ')');
      }
      const byteAddr = index * 4;
      this._counters.recordSharedStore(byteAddr);
      this._f32[index] = value;
      this._written[index] = 1;
    }

    /** Read int32 at index */
    getInt(index) {
      const maxInts = Math.floor(this._sizeBytes / 4);
      if (index < 0 || index >= maxInts) {
        throw new RangeError('SharedMemory OOB i32 read at index ' + index + ' (size ' + maxInts + ')');
      }
      const byteAddr = index * 4;
      this._counters.recordSharedLoad(byteAddr);
      return this._i32[index];
    }

    /** Write int32 at index */
    setInt(index, value) {
      const maxInts = Math.floor(this._sizeBytes / 4);
      if (index < 0 || index >= maxInts) {
        throw new RangeError('SharedMemory OOB i32 write at index ' + index + ' (size ' + maxInts + ')');
      }
      const byteAddr = index * 4;
      this._counters.recordSharedStore(byteAddr);
      this._i32[index] = value;
      this._written[index] = 1;
    }

    /** Check if an index was written (to detect uninitialized reads) */
    isInitialized(index) {
      return this._written[index] === 1;
    }

    /** Get the size in floats */
    get length() {
      return this._f32.length;
    }
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // Atomic Operations
  // ═══════════════════════════════════════════════════════════════════════════

  /** Atomics on a plain typed-array view (a static __shared__ array) instead of a pointer object. */
  function atomicOnArray(proxy, index, op, a, b) {
    const arr = proxy.__raw || proxy;   // atomics are race-free by definition: skip the race detector
    if (index < 0 || index >= arr.length) throw new RangeError('SharedMemory static array OOB atomic at index ' + index + ' (size ' + arr.length + ')');
    const old = arr[index];
    let next = old;
    switch (op) {
      case 'add': next = old + a; break;
      case 'sub': next = old - a; break;
      case 'max': next = Math.max(old, a); break;
      case 'min': next = Math.min(old, a); break;
      case 'exch': next = a; break;
      case 'and': next = old & a; break;
      case 'or': next = old | a; break;
      case 'xor': next = old ^ a; break;
      case 'cas': next = (old === a) ? b : old; break;
    }
    arr[index] = next;
    return old;
  }

  /**
   * All atomics operate on DevicePointer or SharedMemory.
   * They return the old value (CAS-style semantics).
   * Since JS is single-threaded, these are inherently atomic.
   */

  function atomicAdd(ptr, index, val, counters) {
    counters.recordAtomic(ptr._allocId || 0, index);
    if (ptr._f32 === undefined) return atomicOnArray(ptr, index, 'add', val);
    const absIdx = (ptr._offset !== undefined) ? ptr._offset + index : index;
    let old;
    if (ptr instanceof SharedMemory) {
      old = ptr._f32[index];
      ptr._f32[index] = old + val;
    } else {
      old = ptr._f32[absIdx];
      ptr._f32[absIdx] = old + val;
    }
    counters.recordFlop(1);
    return old;
  }

  function atomicSub(ptr, index, val, counters) {
    counters.recordAtomic(ptr._allocId || 0, index);
    if (ptr._f32 === undefined) return atomicOnArray(ptr, index, 'sub', val);
    const absIdx = (ptr._offset !== undefined) ? ptr._offset + index : index;
    let old;
    if (ptr instanceof SharedMemory) {
      old = ptr._f32[index];
      ptr._f32[index] = old - val;
    } else {
      old = ptr._f32[absIdx];
      ptr._f32[absIdx] = old - val;
    }
    return old;
  }

  function atomicMax(ptr, index, val, counters) {
    counters.recordAtomic(ptr._allocId || 0, index);
    if (ptr._f32 === undefined) return atomicOnArray(ptr, index, 'max', val);
    const absIdx = (ptr._offset !== undefined) ? ptr._offset + index : index;
    let old;
    if (ptr instanceof SharedMemory) {
      old = ptr._i32[index];
      ptr._i32[index] = Math.max(old, val);
    } else {
      old = ptr._i32[absIdx];
      ptr._i32[absIdx] = Math.max(old, val);
    }
    return old;
  }

  function atomicMin(ptr, index, val, counters) {
    counters.recordAtomic(ptr._allocId || 0, index);
    if (ptr._f32 === undefined) return atomicOnArray(ptr, index, 'min', val);
    const absIdx = (ptr._offset !== undefined) ? ptr._offset + index : index;
    let old;
    if (ptr instanceof SharedMemory) {
      old = ptr._i32[index];
      ptr._i32[index] = Math.min(old, val);
    } else {
      old = ptr._i32[absIdx];
      ptr._i32[absIdx] = Math.min(old, val);
    }
    return old;
  }

  function atomicCAS(ptr, index, compare, val, counters) {
    counters.recordAtomic(ptr._allocId || 0, index);
    if (ptr._f32 === undefined) return atomicOnArray(ptr, index, 'cas', compare, val);
    const absIdx = (ptr._offset !== undefined) ? ptr._offset + index : index;
    let old;
    if (ptr instanceof SharedMemory) {
      old = ptr._i32[index];
      if (old === compare) ptr._i32[index] = val;
    } else {
      old = ptr._i32[absIdx];
      if (old === compare) ptr._i32[absIdx] = val;
    }
    return old;
  }

  function atomicExch(ptr, index, val, counters) {
    counters.recordAtomic(ptr._allocId || 0, index);
    if (ptr._f32 === undefined) return atomicOnArray(ptr, index, 'exch', val);
    const absIdx = (ptr._offset !== undefined) ? ptr._offset + index : index;
    let old;
    if (ptr instanceof SharedMemory) {
      old = ptr._f32[index];
      ptr._f32[index] = val;
    } else {
      old = ptr._f32[absIdx];
      ptr._f32[absIdx] = val;
    }
    return old;
  }

  function atomicAnd(ptr, index, val, counters) {
    counters.recordAtomic(ptr._allocId || 0, index);
    if (ptr._f32 === undefined) return atomicOnArray(ptr, index, 'and', val);
    const absIdx = (ptr._offset !== undefined) ? ptr._offset + index : index;
    let old;
    if (ptr instanceof SharedMemory) {
      old = ptr._i32[index];
      ptr._i32[index] = old & val;
    } else {
      old = ptr._i32[absIdx];
      ptr._i32[absIdx] = old & val;
    }
    return old;
  }

  function atomicOr(ptr, index, val, counters) {
    counters.recordAtomic(ptr._allocId || 0, index);
    if (ptr._f32 === undefined) return atomicOnArray(ptr, index, 'or', val);
    const absIdx = (ptr._offset !== undefined) ? ptr._offset + index : index;
    let old;
    if (ptr instanceof SharedMemory) {
      old = ptr._i32[index];
      ptr._i32[index] = old | val;
    } else {
      old = ptr._i32[absIdx];
      ptr._i32[absIdx] = old | val;
    }
    return old;
  }

  function atomicXor(ptr, index, val, counters) {
    counters.recordAtomic(ptr._allocId || 0, index);
    if (ptr._f32 === undefined) return atomicOnArray(ptr, index, 'xor', val);
    const absIdx = (ptr._offset !== undefined) ? ptr._offset + index : index;
    let old;
    if (ptr instanceof SharedMemory) {
      old = ptr._i32[index];
      ptr._i32[index] = old ^ val;
    } else {
      old = ptr._i32[absIdx];
      ptr._i32[absIdx] = old ^ val;
    }
    return old;
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // Warp-Level Primitives
  // ═══════════════════════════════════════════════════════════════════════════

  /**
   * Warp shuffle operations operate on a virtual "warp register file".
   * Since we execute threads sequentially, we buffer warp results and
   * replay shuffles from the register file.
   */

  class WarpState {
    constructor() {
      /** Per-lane register values for shuffle: warpId → laneId → value */
      this._registers = new Map();
      /** Per-lane ballot predicate values */
      this._ballots = new Map();
    }

    /**
     * Store a thread's register value for shuffle ops.
     * @param {number} warpId
     * @param {number} laneId
     * @param {*} val
     */
    setRegister(warpId, laneId, val) {
      if (!this._registers.has(warpId)) {
        this._registers.set(warpId, new Float64Array(WARP_SIZE));
      }
      this._registers.get(warpId)[laneId] = val;
    }

    getRegister(warpId, laneId) {
      const regs = this._registers.get(warpId);
      if (!regs) return 0;
      return regs[laneId];
    }

    clear() {
      this._registers.clear();
      this._ballots.clear();
    }
  }

  /**
   * Shuffle down: each lane reads from lane + delta.
   * Used in warp-level reductions.
   */
  function __shfl_down_sync(mask, val, delta, width, warpState, warpId, laneId) {
    const w = width || WARP_SIZE;
    const segment = Math.floor(laneId / w) * w;
    const srcLane = laneId + delta;
    if (srcLane < segment + w) {
      warpState.setRegister(warpId, laneId, val);
      return warpState.getRegister(warpId, srcLane);
    }
    return val;
  }

  /** Shuffle up: each lane reads from lane - delta */
  function __shfl_up_sync(mask, val, delta, width, warpState, warpId, laneId) {
    const w = width || WARP_SIZE;
    const segment = Math.floor(laneId / w) * w;
    const srcLane = laneId - delta;
    if (srcLane >= segment) {
      warpState.setRegister(warpId, laneId, val);
      return warpState.getRegister(warpId, srcLane);
    }
    return val;
  }

  /** Shuffle xor: each lane reads from lane ^ laneMask */
  function __shfl_xor_sync(mask, val, laneMask, width, warpState, warpId, laneId) {
    warpState.setRegister(warpId, laneId, val);
    const w = width || WARP_SIZE;
    const segment = Math.floor(laneId / w) * w;
    const srcLane = segment + ((laneId - segment) ^ laneMask);
    if (srcLane < segment + w) {
      return warpState.getRegister(warpId, srcLane);
    }
    return val;
  }

  /** Shuffle: each lane reads from srcLane */
  function __shfl_sync(mask, val, srcLane, width, warpState, warpId, laneId) {
    warpState.setRegister(warpId, laneId, val);
    const w = width || WARP_SIZE;
    const segment = Math.floor(laneId / w) * w;
    const effSrc = segment + (srcLane % w);
    return warpState.getRegister(warpId, effSrc);
  }

  /** Ballot: returns bitmask of lanes with predicate true */
  function __ballot_sync(mask, predicate, warpState, warpId, laneId) {
    // Store this lane's predicate
    if (!warpState._ballots.has(warpId)) {
      warpState._ballots.set(warpId, new Uint32Array(1));
    }
    const bitmask = warpState._ballots.get(warpId);
    if (predicate) {
      bitmask[0] |= (1 << laneId);
    } else {
      bitmask[0] &= ~(1 << laneId);
    }
    return bitmask[0] & mask;
  }

  /** All sync: returns true if all lanes in mask have predicate true */
  function __all_sync(mask, predicate, warpState, warpId, laneId) {
    const ballot = __ballot_sync(mask, predicate, warpState, warpId, laneId);
    return (ballot & mask) === mask;
  }

  /** Any sync: returns true if any lane in mask has predicate true */
  function __any_sync(mask, predicate, warpState, warpId, laneId) {
    const ballot = __ballot_sync(mask, predicate, warpState, warpId, laneId);
    return (ballot & mask) !== 0;
  }

  /** Population count – number of set bits */
  function __popc(val) {
    let v = val >>> 0;
    v = v - ((v >>> 1) & 0x55555555);
    v = (v & 0x33333333) + ((v >>> 2) & 0x33333333);
    return (((v + (v >>> 4)) & 0x0F0F0F0F) * 0x01010101) >>> 24;
  }

  /** Count leading zeros */
  function __clz(val) {
    return Math.clz32(val >>> 0);
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // CUDA Math Functions
  // ═══════════════════════════════════════════════════════════════════════════

  /** Build the math context object for kernel execution */
  function buildMathContext() {
    return {
      // FP16 & BF16 Half Precision Intrinsics
      __float2half: (FP16 && FP16.float2half) || function(x) { return x; },
      __half2float: (FP16 && FP16.half2float) || function(x) { return x; },
      __float2bfloat16: (FP16 && FP16.float2bfloat16) || function(x) { return x; },
      __bfloat162float: (FP16 && FP16.bfloat162float) || function(x) { return x; },
      __hadd: (FP16 && FP16.__hadd) || function(a, b) { return a + b; },
      __hsub: (FP16 && FP16.__hsub) || function(a, b) { return a - b; },
      __hmul: (FP16 && FP16.__hmul) || function(a, b) { return a * b; },
      __hdiv: (FP16 && FP16.__hdiv) || function(a, b) { return a / b; },
      __hneg: (FP16 && FP16.__hneg) || function(a) { return -a; },
      __hadd_bf16: (FP16 && FP16.__hadd_bf16) || function(a, b) { return a + b; },
      __hsub_bf16: (FP16 && FP16.__hsub_bf16) || function(a, b) { return a - b; },
      __hmul_bf16: (FP16 && FP16.__hmul_bf16) || function(a, b) { return a * b; },
      __hdiv_bf16: (FP16 && FP16.__hdiv_bf16) || function(a, b) { return a / b; },
      __hneg_bf16: (FP16 && FP16.__hneg_bf16) || function(a) { return -a; },
      // Standard math functions
      expf: Math.exp,
      logf: Math.log,
      sqrtf: Math.sqrt,
      rsqrtf: function (x) { return 1.0 / Math.sqrt(x); },
      fabsf: Math.abs,
      fmaxf: Math.max,
      fminf: Math.min,
      powf: Math.pow,
      sinf: Math.sin,
      cosf: Math.cos,
      tanf: Math.tan,
      tanhf: Math.tanh,
      ceilf: Math.ceil,
      floorf: Math.floor,
      roundf: Math.round,

      // Floating-point classification & sign
      isinf: function (x) { return !Number.isFinite(x) && !Number.isNaN(x); },
      isinff: function (x) { return !Number.isFinite(x) && !Number.isNaN(x); },
      __isinf: function (x) { return !Number.isFinite(x) && !Number.isNaN(x); },
      __isinff: function (x) { return !Number.isFinite(x) && !Number.isNaN(x); },
      isnan: Number.isNaN,
      isnanf: Number.isNaN,
      __isnan: Number.isNaN,
      __isnanf: Number.isNaN,
      isfinite: Number.isFinite,
      isfinitef: Number.isFinite,
      __finite: Number.isFinite,
      __finitef: Number.isFinite,
      signbit: function (x) { return Math.sign(x) < 0 || Object.is(x, -0); },
      signbitf: function (x) { return Math.sign(x) < 0 || Object.is(x, -0); },

      // Additional math operations
      hypot: Math.hypot,
      hypotf: Math.hypot,
      cbrt: Math.cbrt,
      cbrtf: Math.cbrt,
      expm1: Math.expm1,
      expm1f: Math.expm1,
      log1p: Math.log1p,
      log1pf: Math.log1p,
      exp2: function (x) { return Math.pow(2, x); },
      exp2f: function (x) { return Math.pow(2, x); },
      exp10: function (x) { return Math.pow(10, x); },
      exp10f: function (x) { return Math.pow(10, x); },
      __exp10f: function (x) { return Math.pow(10, x); },
      fmod: function (a, b) { return a % b; },
      fmodf: function (a, b) { return a % b; },

      // Fast-math intrinsics (same implementations for simulation)
      __expf: Math.exp,
      __logf: Math.log,
      __fdividef: function (a, b) { return a / b; },
      __fmaf_rn: function (a, b, c) { return Math.fround(a * b + c); },
      __fsqrt_rn: function (x) { return Math.fround(Math.sqrt(x)); },

      // FMA
      fma: function (a, b, c) { return a * b + c; },
      fmaf: function (a, b, c) { return Math.fround(a * b + c); },
      copysignf: function (mag, sgn) {
        return Math.sign(sgn) === 0 ? mag : Math.abs(mag) * Math.sign(sgn);
      },

      // Constants
      INFINITY: CUDA_INFINITY,
      NAN: CUDA_NAN,
      FLT_MAX: CUDA_FLT_MAX,
      FLT_MIN: CUDA_FLT_MIN,
      FLT_EPSILON: CUDA_FLT_EPSILON,
      M_PI: CUDA_M_PI,
      M_PI_2: CUDA_M_PI_2,
      M_SQRT2: CUDA_M_SQRT2
    };
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // KernelLauncher — executes transpiled CUDA kernels
  // ═══════════════════════════════════════════════════════════════════════════

  class KernelLauncher {
    /**
     * @param {SimCounters} counters
     * @param {object}      gpuProfile
     * @param {number}      [deviceId=0]
     */
    constructor(counters, gpuProfile, deviceId = 0) {
      this._counters = counters;
      this._gpuProfile = gpuProfile;
      this._deviceId = deviceId;
      this._multiGPU = null;
      this._diagnostics = [];
      this._lastError = null;
      this._warpState = new WarpState();
      this._mathContext = buildMathContext();
    }

    setMultiGPU(multiGPU) {
      this._multiGPU = multiGPU;
    }

    /**
     * Launch a kernel across the full grid.
     *
     * The transpiled kernel function signature:
     *   function(threadIdx, blockIdx, blockDim, gridDim, __shared, __syncthreads,
     *            __atomicAdd, __printf, ...userArgs)
     *
     * Additionally, warp intrinsics, math functions, and other atomics are
     * injected via the execution context.
     *
     * @param {Function} kernelFn  – Transpiled kernel function
     * @param {object}   gridDim   – Grid dimensions {x, y, z}
     * @param {object}   blockDim  – Block dimensions {x, y, z}
     * @param {number}   sharedMemBytes – Dynamic shared memory in bytes
     * @param {...*}     kernelArgs – User kernel arguments
     */
    launch(kernelFn, gridDim, blockDim, sharedMemBytes, ...kernelArgs) {
      this._lastError = null;
      const self = this;
      const grid = dim3(gridDim);
      const block = dim3(blockDim);
      const totalBlocks = dim3Volume(grid);
      const threadsPerBlock = dim3Volume(block);
      const counters = this._counters;
      const diag = this._diagnostics;
      const warpState = this._warpState;

      if (totalBlocks <= 0 || threadsPerBlock <= 0) {
        const err = new Error('cudaErrorInvalidConfiguration: invalid grid or block dimension (grid=' + totalBlocks + ', block=' + threadsPerBlock + ')');
        diag.push({
          type: 'error',
          category: 'cudaErrorInvalidConfiguration',
          kernel: (kernelFn.name || 'anonymous_kernel').replace(/^__kernel_/, ''),
          message: err.message,
          block: { x: 0, y: 0, z: 0 },
          thread: { x: 0, y: 0, z: 0 }
        });
        this._lastError = err.message;
        throw err;
      }
      if (threadsPerBlock > 1024) {
        const err = new Error('cudaErrorInvalidConfiguration: threads per block (' + threadsPerBlock + ') exceeds hardware maximum 1024');
        diag.push({
          type: 'error',
          category: 'cudaErrorInvalidConfiguration',
          kernel: (kernelFn.name || 'anonymous_kernel').replace(/^__kernel_/, ''),
          message: err.message,
          block: { x: 0, y: 0, z: 0 },
          thread: { x: 0, y: 0, z: 0 }
        });
        this._lastError = err.message;
        throw err;
      }
      if (typeof sharedMemBytes === 'number' && sharedMemBytes < 0) {
        const err = new Error('cudaErrorInvalidConfiguration: dynamic shared memory cannot be negative (' + sharedMemBytes + ')');
        diag.push({
          type: 'error',
          category: 'cudaErrorInvalidConfiguration',
          kernel: (kernelFn.name || 'anonymous_kernel').replace(/^__kernel_/, ''),
          message: err.message,
          block: { x: 0, y: 0, z: 0 },
          thread: { x: 0, y: 0, z: 0 }
        });
        this._lastError = err.message;
        throw err;
      }

      // Cross-device pointer validation
      if (this._deviceId !== undefined && this._multiGPU) {
        for (const arg of kernelArgs) {
          if (arg && arg._deviceId !== undefined) {
            if (arg._deviceId !== this._deviceId && !this._multiGPU.hasPeerAccess(this._deviceId, arg._deviceId)) {
              const err = new Error('cudaErrorIllegalAddress: cross-device memory access: pointer belongs to GPU ' + arg._deviceId + ' but launched on GPU ' + this._deviceId + ' without peer access');
              diag.push({
                type: 'error',
                category: 'cudaErrorIllegalAddress',
                kernel: (kernelFn.name || 'anonymous_kernel').replace(/^__kernel_/, ''),
                message: err.message,
                block: { x: 0, y: 0, z: 0 },
                thread: { x: 0, y: 0, z: 0 }
              });
              this._lastError = err.message;
              throw err;
            }
          }
        }
      }

      counters.blocksLaunched += totalBlocks;
      counters.threadsLaunched += totalBlocks * threadsPerBlock;

      // Pre-allocated shared memory size (minimum 256 bytes)
      const shmemSize = Math.max(sharedMemBytes || 256, 256);

      // Iterate over every block in the grid
      for (let bz = 0; bz < grid.z; bz++) {
        for (let by = 0; by < grid.y; by++) {
          for (let bx = 0; bx < grid.x; bx++) {
            const blockIdx = { x: bx, y: by, z: bz };

            // Allocate shared memory for this block
            const sharedMem = new SharedMemory(shmemSize, counters);

            // Sync barrier tracking: kernels that call __syncthreads
            // are run in phases. We collect per-thread continuations.
            // Since JS is single-threaded and we can't truly do barriers
            // within a single function call, we use a multi-pass approach:
            // Phase 1: run all threads until first __syncthreads
            // Phase 2: run all threads until next __syncthreads (or end)
            // etc.

            // We'll execute threads using a coroutine-like approach via
            // generators if the kernel yields at __syncthreads. For
            // simple kernels without __syncthreads, direct execution.

            // Collect warp-level global access addresses per warp for
            // coalescing analysis
            const warpAccesses = new Map(); // warpId → [byteAddresses]

            // Build the execution context that threads receive
            const self = this;

            // __syncthreads sentinel
            const SYNC_SENTINEL = Symbol('__syncthreads');

            // Detect if the kernel uses generators (__syncthreads)
            // We'll try generator-based execution first, fall back to direct.
            let useGenerators = false;
            let threadGens = [];

            // === Phase-based execution with __syncthreads support ===

            // First, determine the linear thread ordering
            const threadIndices = [];
            for (let tz = 0; tz < block.z; tz++) {
              for (let ty = 0; ty < block.y; ty++) {
                for (let tx = 0; tx < block.x; tx++) {
                  threadIndices.push({ x: tx, y: ty, z: tz });
                }
              }
            }

            // Build intrinsics for each thread
            const buildThreadContext = (threadIdx) => {
              const currentThreadIdx = { x: threadIdx.x || 0, y: threadIdx.y || 0, z: threadIdx.z || 0 };
              const linearIdx = threadIdx.x + threadIdx.y * block.x + threadIdx.z * block.x * block.y;
              const warpId = Math.floor(linearIdx / WARP_SIZE);
              const laneId = linearIdx % WARP_SIZE;

              // Printf for kernel debugging
              const __printf = function (...args) {
                if (args.length === 0) return;
                let fmt = String(args[0]);
                let argIdx = 1;
                let formatted = fmt.replace(/%([0-9]*\.?[0-9]*[dfsuxXgG%])/g, (match, spec) => {
                  if (spec === '%') return '%';
                  if (argIdx >= args.length) return match;
                  const val = args[argIdx++];
                  if (spec.endsWith('f') || spec.endsWith('g') || spec.endsWith('G')) {
                    const precision = spec.includes('.') ? parseInt(spec.split('.')[1]) : 6;
                    return Number(val).toFixed(precision);
                  }
                  if (spec.endsWith('d') || spec.endsWith('i') || spec.endsWith('u')) {
                    return parseInt(val, 10);
                  }
                  if (spec.endsWith('x') || spec.endsWith('X')) {
                    return (val >>> 0).toString(16);
                  }
                  return String(val);
                });
                if (argIdx < args.length) {
                  formatted += ' ' + args.slice(argIdx).join(' ');
                }
                diag.push({
                  type: 'printf',
                  message: formatted,
                  block: { ...blockIdx },
                  thread: { ...threadIdx }
                });
              };

              // Atomic operations bound to this runtime's counters
              const __atomicAdd = (ptr, idx, val) => atomicAdd(ptr, idx, val, counters);
              const __atomicSub = (ptr, idx, val) => atomicSub(ptr, idx, val, counters);
              const __atomicMax = (ptr, idx, val) => atomicMax(ptr, idx, val, counters);
              const __atomicMin = (ptr, idx, val) => atomicMin(ptr, idx, val, counters);
              const __atomicCAS = (ptr, idx, cmp, val) => atomicCAS(ptr, idx, cmp, val, counters);
              const __atomicExch = (ptr, idx, val) => atomicExch(ptr, idx, val, counters);
              const __atomicAnd = (ptr, idx, val) => atomicAnd(ptr, idx, val, counters);
              const __atomicOr = (ptr, idx, val) => atomicOr(ptr, idx, val, counters);
              const __atomicXor = (ptr, idx, val) => atomicXor(ptr, idx, val, counters);

              // Warp primitives bound to this thread's warp/lane
              const __shfl_down = (mask, val, delta, width) =>
                __shfl_down_sync(mask, val, delta, width, warpState, warpId, laneId);
              const __shfl_up = (mask, val, delta, width) =>
                __shfl_up_sync(mask, val, delta, width, warpState, warpId, laneId);
              const __shfl_xor = (mask, val, laneMask, width) =>
                __shfl_xor_sync(mask, val, laneMask, width, warpState, warpId, laneId);
              const __shfl = (mask, val, srcLane, width) =>
                __shfl_sync(mask, val, srcLane, width, warpState, warpId, laneId);
              const __ballot = (mask, pred) =>
                __ballot_sync(mask, pred, warpState, warpId, laneId);
              const __all = (mask, pred) =>
                __all_sync(mask, pred, warpState, warpId, laneId);
              const __any = (mask, pred) =>
                __any_sync(mask, pred, warpState, warpId, laneId);

              const __atomic = function (ptr, idx, val) { return atomicAdd(ptr, idx, val, counters); };
              __atomic.add = (ptr, idx, val) => atomicAdd(ptr, idx, val, counters);
              __atomic.sub = (ptr, idx, val) => atomicSub(ptr, idx, val, counters);
              __atomic.max = (ptr, idx, val) => atomicMax(ptr, idx, val, counters);
              __atomic.min = (ptr, idx, val) => atomicMin(ptr, idx, val, counters);
              __atomic.cas = (ptr, idx, cmp, val) => atomicCAS(ptr, idx, cmp, val, counters);
              __atomic.exch = (ptr, idx, val) => atomicExch(ptr, idx, val, counters);
              __atomic.and = (ptr, idx, val) => atomicAnd(ptr, idx, val, counters);
              __atomic.or = (ptr, idx, val) => atomicOr(ptr, idx, val, counters);
              __atomic.xor = (ptr, idx, val) => atomicXor(ptr, idx, val, counters);
              __atomic.br = (site, cond) => { counters.recordBranch(site, !!cond); return cond; };
              __atomic.fl = (n) => { counters.recordFlops(n); };

              return {
                threadIdx: currentThreadIdx,
                __printf,
                __atomic,
                __atomicAdd, __atomicSub, __atomicMax, __atomicMin,
                __atomicCAS, __atomicExch, __atomicAnd, __atomicOr, __atomicXor,
                __shfl_down_sync: __shfl_down,
                __shfl_up_sync: __shfl_up,
                __shfl_xor_sync: __shfl_xor,
                __shfl_sync: __shfl,
                __ballot_sync: __ballot,
                __all_sync: __all,
                __any_sync: __any,
                __popc,
                __clz,
                linearIdx,
                warpId,
                laneId
              };
            };

            // Try executing with sync barriers (phase-based)
            // We use a simple model: all threads run between barriers.
            // __syncthreads is passed as a callback that records the phase.

            // Since generators aren't guaranteed, we use a simpler model:
            // Collect all sync points by running each thread in sequence,
            // and use a phase counter to coordinate.

            // Execute block threads via SIMT coroutines or sequential fallback
            const threadContexts = [];
            let isGenerator = false;
            let stepCount = 0;
            const maxSteps = this.maxSteps || 50000;
            const maxTimeMs = this.maxTimeMs || 2000;
            const launchStartTime = Date.now();

            // Check for block thread boundary divergence
            if (threadsPerBlock % WARP_SIZE !== 0) {
              counters.recordDivergentBranch();
            }

            for (let t = 0; t < threadIndices.length; t++) {
              const threadIdx = threadIndices[t];
              const ctx = buildThreadContext(threadIdx);

              const __syncthreads = function* () {
                counters.syncthreadsCount++;
                // warp access windows are flushed when the whole block reaches the barrier
                yield { type: 'sync' };
              };

              // Warp primitives that yield for warp-wide lane exchange
              const __warp_shfl_down = function* (mask, val, delta, width) {
                return yield { type: 'shfl', op: 'down', mask, val, delta, width, warpId: ctx.warpId, laneId: ctx.laneId };
              };
              const __warp_shfl = function* (mask, val, srcLane, width) {
                return yield { type: 'shfl', op: 'sync', mask, val, srcLane, width, warpId: ctx.warpId, laneId: ctx.laneId };
              };
              const __warp_shfl_up = function* (mask, val, delta, width) {
                return yield { type: 'shfl', op: 'up', mask, val, delta, width, warpId: ctx.warpId, laneId: ctx.laneId };
              };
              const __warp_shfl_xor = function* (mask, val, laneMask, width) {
                return yield { type: 'shfl', op: 'xor', mask, val, laneMask, width, warpId: ctx.warpId, laneId: ctx.laneId };
              };
              const __warp_ballot = function* (mask, pred) {
                return yield { type: 'ballot', mask, pred, warpId: ctx.warpId, laneId: ctx.laneId };
              };

              const boundThis = Object.assign({}, self._mathContext, ctx, {
                __sync: __syncthreads,
                __syncthreads: __syncthreads,
                __shfl_down_sync: __warp_shfl_down,
                __shfl_sync: __warp_shfl,
                __shfl_up_sync: __warp_shfl_up,
                __shfl_xor_sync: __warp_shfl_xor,
                __ballot_sync: __warp_ballot,
              });

              try {
                counters.setActiveContext(ctx.warpId, ctx.linearIdx);
                if (sharedMem && sharedMem.setActiveContext) sharedMem.setActiveContext(ctx);
                const res = kernelFn.call(
                  boundThis,
                  threadIdx,
                  blockIdx,
                  block,
                  grid,
                  sharedMem,
                  __syncthreads,
                  ctx.__atomic,
                  ctx.__printf,
                  ...kernelArgs
                );
                counters.clearActiveContext();

                if (res && typeof res.next === 'function') {
                  isGenerator = true;
                  threadContexts.push({
                    t,
                    threadIdx,
                    ctx,
                    gen: res,
                    done: false,
                    blocked: false,
                    pendingOp: null,
                    nextVal: undefined
                  });
                }
              } catch (err) {
                counters.clearActiveContext();
                const category = err.name || 'RuntimeError';
                const kName = (kernelFn.name || 'anonymous_kernel').replace(/^__kernel_/, '');
                diag.push({
                  type: 'error',
                  category: category,
                  kernel: kName,
                  message: err.message,
                  stack: err.stack,
                  block: { ...blockIdx },
                  thread: { ...threadIdx }
                });
                self._lastError = err.message;
              }
            }

            if (isGenerator) {
              // SIMT Coroutine Engine: Run all threads in lockstep
              let running = true;
              while (running) {
                running = false;
                stepCount++;
                if (stepCount > maxSteps || (stepCount % 500 === 0 && (Date.now() - launchStartTime) > maxTimeMs)) {
                  const kName = (kernelFn.name || 'anonymous_kernel').replace(/^__kernel_/, '');
                  const offendingThread = threadContexts.find(th => !th.done) || threadContexts[0];
                  throw new Error(`watchdog timeout: kernel "${kName}" exceeded step limit (${maxSteps} steps) at block (${blockIdx.x},${blockIdx.y},${blockIdx.z}) thread (${offendingThread.threadIdx.x},${offendingThread.threadIdx.y},${offendingThread.threadIdx.z})`);
                }

                // Step each unblocked thread
                for (const th of threadContexts) {
                  if (!th.done && !th.blocked) {
                    try {
                      counters.setActiveContext(th.ctx.warpId, th.ctx.linearIdx);
                      if (sharedMem && sharedMem.setActiveContext) sharedMem.setActiveContext(th.ctx);
                      const step = th.gen.next(th.nextVal);
                      counters.clearActiveContext();
                      th.nextVal = undefined;
                      if (step.done) {
                        th.done = true;
                      } else {
                        running = true;
                        const v = step.value;
                        if (v && v.type === 'sync') {
                          th.blocked = true;
                        } else if (v && (v.type === 'shfl' || v.type === 'ballot')) {
                          th.pendingOp = v;
                        }
                      }
                    } catch (err) {
                      counters.clearActiveContext();
                      th.done = true;
                      const category = err.name || 'RuntimeError';
                      const kName = (kernelFn.name || 'anonymous_kernel').replace(/^__kernel_/, '');
                      diag.push({
                        type: 'error',
                        category: category,
                        kernel: kName,
                        message: err.message,
                        stack: err.stack,
                        block: { ...blockIdx },
                        thread: { ...th.threadIdx }
                      });
                      self._lastError = err.message;
                    }
                  }
                }

                // Resolve pending warp operations for this step
                const warpPending = new Map();
                for (const th of threadContexts) {
                  if (th.pendingOp) {
                    const wId = th.ctx.warpId;
                    if (!warpPending.has(wId)) warpPending.set(wId, []);
                    warpPending.get(wId).push(th);
                  }
                }

                for (const [wId, thList] of warpPending.entries()) {
                  // Buffer registers across this warp
                  const warpRegisters = new Float64Array(WARP_SIZE);
                  for (const th of thList) {
                    warpRegisters[th.ctx.laneId] = th.pendingOp.val;
                  }

                  // Deliver shuffle / ballot results
                  for (const th of thList) {
                    const op = th.pendingOp;
                    const lane = th.ctx.laneId;
                    const w = op.width || WARP_SIZE;
                    const segment = Math.floor(lane / w) * w;

                    if (op.op === 'down') {
                      const srcLane = lane + op.delta;
                      th.nextVal = (srcLane < segment + w) ? warpRegisters[srcLane] : op.val;
                    } else if (op.op === 'up') {
                      const srcLane = lane - op.delta;
                      th.nextVal = (srcLane >= segment) ? warpRegisters[srcLane] : op.val;
                    } else if (op.op === 'xor') {
                      const srcLane = segment + ((lane - segment) ^ op.laneMask);
                      th.nextVal = (srcLane < segment + w) ? warpRegisters[srcLane] : op.val;
                    } else if (op.op === 'sync') {
                      const srcLane = segment + (op.srcLane % w);
                      th.nextVal = warpRegisters[srcLane];
                    } else if (op.type === 'ballot') {
                      let mask = 0;
                      for (const otherTh of thList) {
                        if (otherTh.pendingOp.pred) mask |= (1 << otherTh.ctx.laneId);
                      }
                      const expectedMask = op.mask || 0xFFFFFFFF;
                      if (mask !== 0 && mask !== expectedMask) {
                        counters.recordDivergentBranch();
                      }
                      th.nextVal = mask & expectedMask;
                    }
                    th.pendingOp = null;
                  }
                }

                // Advance barrier: if all living threads are blocked at sync, wake them all
                const living = threadContexts.filter(t => !t.done);
                if (living.length > 0 && living.every(t => t.blocked)) {
                  if (living.length < threadContexts.length) {
                    const kName = (kernelFn.name || 'anonymous_kernel').replace(/^__kernel_/, '');
                    const errDiag = {
                      type: 'error',
                      category: 'BarrierDivergenceError',
                      kernel: kName,
                      message: `Barrier divergence detected in kernel "${kName}": __syncthreads() called conditionally; only ${living.length} of ${threadContexts.length} threads in block reached barrier`,
                      block: { ...blockIdx },
                      thread: { ...living[0].threadIdx }
                    };
                    diag.push(errDiag);
                    self._lastError = errDiag.message;
                  }
                  if (sharedMem && sharedMem._raceDetector) {
                    sharedMem._raceDetector.advanceBarrier();
                  }
                  counters.flushSharedBankAccesses();
                  counters.flushWarpGlobalAccesses();
                  for (const th of living) th.blocked = false;
                }
              }
            }

            // Flush remaining shared bank and warp global analyses
            counters.flushSharedBankAccesses();
            counters.flushWarpGlobalAccesses();
            warpState.clear();
          }
        }
      }
    }

    /** Get diagnostics (printf output, errors) from the last launch */
    getDiagnostics() {
      return this._diagnostics;
    }

    /** Clear diagnostics */
    clearDiagnostics() {
      this._diagnostics = [];
      this._lastError = null;
    }
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // MultiGPURuntime — multi-device simulation with NCCL collectives
  // ═══════════════════════════════════════════════════════════════════════════

  class NcclComm {
    /**
     * @param {number} nranks – Number of ranks in the communicator
     * @param {number} rank   – This rank's index
     * @param {MultiGPURuntime} runtime
     * @param {object} [clique] - Shared collective state among group
     * @param {object} [options] - Options (algorithm, deviceIds, commId)
     */
    constructor(nranks, rank, runtime, clique, options = {}) {
      this.nranks = nranks;
      this.rank = rank;
      this._runtime = runtime;
      this.algorithm = options.algorithm || null;
      this.deviceIds = options.deviceIds || options.ranks || null;
      this.commId = options.commId || 0;
      this._clique = clique || {
        nranks,
        pendingAllReduce: [],
        pendingBroadcast: [],
        pendingReduceScatter: [],
        pendingAllGather: [],
        pendingReduce: []
      };
    }
  }

  class MultiGPURuntime {
    /**
     * @param {number} numDevices – Number of simulated GPUs
     * @param {object} gpuProfile
     */
    constructor(numDevices, gpuProfile) {
      this._numDevices = numDevices;
      this._currentDevice = 0;
      this._gpuProfile = gpuProfile;

      /** Per-device state: memory arenas, counters, launchers */
      this._devices = [];
      for (let i = 0; i < numDevices; i++) {
        const counters = new SimCounters(gpuProfile);
        const memory = new SimMemory(counters, i);
        const launcher = new KernelLauncher(counters, gpuProfile, i);
        launcher.setMultiGPU(this);
        this._devices.push({ counters, memory, launcher });
      }

      /** Peer access enabled pairs: "src:dst" → true */
      this._peerAccess = new Set();
    }

    hasPeerAccess(devA, devB) {
      if (devA === devB) return true;
      return this._peerAccess.has(`${devA}:${devB}`);
    }

    /** cudaSetDevice */
    cudaSetDevice(id) {
      if (id < 0 || id >= this._numDevices) {
        throw new Error('cudaErrorInvalidDevice: invalid device ordinal ' + id + ' for cluster of size ' + this._numDevices);
      }
      this._currentDevice = id;
    }

    /** cudaGetDevice */
    cudaGetDevice() {
      return this._currentDevice;
    }

    /** Get the current device's state */
    _dev(id) {
      const i = (id !== undefined) ? id : this._currentDevice;
      return this._devices[i];
    }

    /** cudaDeviceEnablePeerAccess */
    cudaDeviceEnablePeerAccess(peer, flags) {
      if (peer < 0 || peer >= this._numDevices) {
        throw new Error('cudaErrorInvalidDevice: invalid peer device ' + peer);
      }
      if (peer === this._currentDevice) {
        throw new Error('cudaErrorInvalidDevice: cannot enable peer access to self');
      }
      this._peerAccess.add(this._currentDevice + ':' + peer);
      return 0;
    }

    /** cudaDeviceDisablePeerAccess */
    cudaDeviceDisablePeerAccess(peer) {
      this._peerAccess.delete(this._currentDevice + ':' + peer);
      return 0;
    }

    /**
     * cudaMemcpyPeer — copy between devices.
     * @param {DevicePointer} dst
     * @param {number} dstDev
     * @param {DevicePointer} src
     * @param {number} srcDev
     * @param {number} sizeBytes
     */
    cudaMemcpyPeer(dst, dstDev, src, srcDev, sizeBytes) {
      if (srcDev < 0 || srcDev >= this._numDevices) throw new Error('cudaErrorInvalidDevice: invalid srcDev ' + srcDev);
      if (dstDev < 0 || dstDev >= this._numDevices) throw new Error('cudaErrorInvalidDevice: invalid dstDev ' + dstDev);
      if (!src) throw new Error('cudaErrorInvalidValue: null src pointer in cudaMemcpyPeer');
      if (!dst) throw new Error('cudaErrorInvalidValue: null dst pointer in cudaMemcpyPeer');
      if (typeof sizeBytes !== 'number' || sizeBytes < 0) throw new Error('cudaErrorInvalidValue: invalid or negative sizeBytes');

      const srcU8 = new Uint8Array(src._buffer, src._offset * src._elementSize, sizeBytes);
      const dstU8 = new Uint8Array(dst._buffer, dst._offset * dst._elementSize);
      dstU8.set(srcU8.subarray(0, sizeBytes));

      // Track cross-GPU bytes: each communicating device records transferred bytes (egress / ingress)
      this._devices[srcDev].counters.crossGpuBytes += sizeBytes;
      this._devices[dstDev].counters.crossGpuBytes += sizeBytes;
    }

    /** ncclCommInitRank */
    ncclCommInitRank(nranks, rank, options = {}) {
      if (Array.isArray(options)) {
        options = { deviceIds: options };
      }
      return new NcclComm(nranks, rank, this, null, options);
    }

    /** ncclCommInitAll */
    ncclCommInitAll(comms, nranks, options = {}) {
      const clique = {
        nranks,
        pendingAllReduce: [],
        pendingBroadcast: [],
        pendingReduceScatter: [],
        pendingAllGather: [],
        pendingReduce: []
      };
      for (let r = 0; r < nranks; r++) {
        const comm = new NcclComm(nranks, r, this, clique, options);
        if (comms && (Array.isArray(comms) || typeof comms === 'object')) {
          comms[r] = comm;
        }
      }
      return comms;
    }

    /** Per-rank collective calls are checked against the other ranks' calls as they arrive:
     *  the n-th collective on a communicator must have the same kind, count, type, root and op on every rank. */
    _trackCollective(comm, rank, nranks, op, count, datatype, root, reduceOp) {
      const D = DesyncModule && (DesyncModule.CollectiveDesyncDetector || (DesyncModule.default && DesyncModule.default.CollectiveDesyncDetector));
      if (!D) return;
      if (!this._desyncDetector) this._desyncDetector = new D();
      this._desyncDetector.postCollective({ commId: (comm && comm.id) || 0, nranks, rank, op, count, datatype, root, reduceOp });
    }

    /**
     * ncclAllReduce — all-reduce across devices.
     * @param {DevicePointer[]|DevicePointer} sendbufs – Per-rank send buffers (or single DevicePointer for current rank)
     * @param {DevicePointer[]|DevicePointer} recvbufs – Per-rank receive buffers (or single DevicePointer for current rank)
     * @param {number} count – Number of float elements
     * @param {string} datatype – 'float32'
     * @param {string} op – 'sum', 'prod', 'max', 'min', 'avg'
     * @param {NcclComm} comm
     */
    ncclAllReduce(sendbufs, recvbufs, count, datatype, op, comm) {
      if (count < 0) throw new Error('ncclInvalidArgument: count must be non-negative');
      op = (typeof op === 'string' ? op.toLowerCase() : 'sum');

      // If called per-rank with a single buffer, stage until all ranks arrive
      if (!Array.isArray(sendbufs)) {
        const nranks = (comm && comm.nranks) ? comm.nranks : this._numDevices;
        const rank = (comm && comm.rank !== undefined) ? comm.rank : this._currentDevice;
        if (rank < 0 || rank >= nranks) throw new Error('ncclInvalidArgument: invalid rank ' + rank + ' for comm with ' + nranks + ' ranks');
        const clique = (comm && comm._clique) ? comm._clique : (this._defaultClique || (this._defaultClique = {
          nranks,
          pendingAllReduce: [],
          pendingBroadcast: [],
          pendingReduceScatter: [],
          pendingAllGather: []
        }));
        this._trackCollective(comm, rank, nranks, 'allreduce', count, datatype, undefined, op);
        clique.pendingAllReduce[rank] = { sendbuf: sendbufs, recvbuf: recvbufs, count, datatype, op, comm };
        let ready = true;
        for (let r = 0; r < nranks; r++) {
          if (!clique.pendingAllReduce[r]) { ready = false; break; }
        }
        if (ready) {
          const staged = clique.pendingAllReduce;
          clique.pendingAllReduce = [];
          const allSends = staged.map(s => s.sendbuf);
          const allRecvs = staged.map(s => s.recvbuf);
          return this.ncclAllReduce(allSends, allRecvs, count, datatype, op, comm || { nranks });
        }
        return 0;
      }

      const nranks = (comm && comm.nranks) ? comm.nranks : (Array.isArray(sendbufs) ? sendbufs.length : this._numDevices);
      if (sendbufs.length !== nranks) throw new Error('ncclInvalidArgument: sendbufs length (' + sendbufs.length + ') must match comm.nranks (' + nranks + ')');
      if (recvbufs.length !== nranks) throw new Error('ncclInvalidArgument: recvbufs length (' + recvbufs.length + ') must match comm.nranks (' + nranks + ')');

      if (count === 0) {
        for (let r = 0; r < nranks; r++) this._devices[r].counters.ncclOps++;
        return 0;
      }

      // Collect all values
      const reduced = new Float32Array(count);

      // Initialize with identity element
      if (op === 'sum' || op === 'avg') reduced.fill(0);
      else if (op === 'prod') reduced.fill(1);
      else if (op === 'max') reduced.fill(-Infinity);
      else if (op === 'min') reduced.fill(Infinity);

      // Reduce across ranks
      for (let r = 0; r < nranks; r++) {
        const src = sendbufs[r];
        for (let i = 0; i < count; i++) {
          const val = src._rawGet(i);
          if (op === 'sum' || op === 'avg') reduced[i] += val;
          else if (op === 'prod') reduced[i] *= val;
          else if (op === 'max') reduced[i] = Math.max(reduced[i], val);
          else if (op === 'min') reduced[i] = Math.min(reduced[i], val);
        }
      }

      if (op === 'avg') {
        for (let i = 0; i < count; i++) reduced[i] /= nranks;
      }

      // Scatter result to all receive buffers
      const bytesPerRank = count * 4;
      const isRing = (comm && comm.algorithm === 'ring') || (this._collectiveAlgorithm === 'ring');
      for (let r = 0; r < nranks; r++) {
        const dst = recvbufs[r];
        for (let i = 0; i < count; i++) {
          dst._rawSet(i, reduced[i]);
        }
        const devR = (comm && comm.deviceIds) ? comm.deviceIds[r] : r;
        if (nranks > 1) {
          if (isRing) {
            this._devices[devR].counters.crossGpuBytes += Math.round(2 * (nranks - 1) / nranks * bytesPerRank);
          } else {
            this._devices[devR].counters.crossGpuBytes += bytesPerRank * (nranks - 1);
          }
        }
        this._devices[devR].counters.ncclOps++;
      }
      return 0;
    }

    /**
     * ncclBroadcast — broadcast from root to all ranks.
     */
    ncclBroadcast(sendbufs, recvbufs, count, datatype, root, comm) {
      if (count < 0) throw new Error('ncclInvalidArgument: count must be non-negative');
      root = (typeof root === 'number' ? root : 0);

      // If called per-rank with a single buffer, stage until all ranks arrive
      if (!Array.isArray(sendbufs)) {
        const nranks = (comm && comm.nranks) ? comm.nranks : this._numDevices;
        const rank = (comm && comm.rank !== undefined) ? comm.rank : this._currentDevice;
        if (rank < 0 || rank >= nranks) throw new Error('ncclInvalidArgument: invalid rank ' + rank + ' for comm with ' + nranks + ' ranks');
        if (root < 0 || root >= nranks) throw new Error('ncclInvalidArgument: invalid root rank ' + root + ' for comm with ' + nranks + ' ranks');
        const clique = (comm && comm._clique) ? comm._clique : (this._defaultClique || (this._defaultClique = {
          nranks,
          pendingAllReduce: [],
          pendingBroadcast: [],
          pendingReduceScatter: [],
          pendingAllGather: [],
          pendingReduce: []
        }));
        this._trackCollective(comm, rank, nranks, 'broadcast', count, datatype, root, undefined);
        clique.pendingBroadcast[rank] = { sendbuf: sendbufs, recvbuf: recvbufs, count, datatype, root, comm };
        let ready = true;
        for (let r = 0; r < nranks; r++) {
          if (!clique.pendingBroadcast[r]) { ready = false; break; }
        }
        if (ready) {
          const staged = clique.pendingBroadcast;
          clique.pendingBroadcast = [];
          const allSends = staged.map(s => s.sendbuf);
          const allRecvs = staged.map(s => s.recvbuf);
          return this.ncclBroadcast(allSends, allRecvs, count, datatype, root, comm || { nranks });
        }
        return 0;
      }

      const nranks = (comm && comm.nranks) ? comm.nranks : (Array.isArray(sendbufs) ? sendbufs.length : this._numDevices);
      if (root < 0 || root >= nranks) throw new Error('ncclInvalidArgument: invalid root rank ' + root + ' for communicator of size ' + nranks);
      if (sendbufs.length !== nranks) throw new Error('ncclInvalidArgument: sendbufs length (' + sendbufs.length + ') must match comm.nranks (' + nranks + ')');
      if (recvbufs.length !== nranks) throw new Error('ncclInvalidArgument: recvbufs length (' + recvbufs.length + ') must match comm.nranks (' + nranks + ')');

      if (count === 0) {
        for (let r = 0; r < nranks; r++) {
          const devR = (comm && comm.deviceIds) ? comm.deviceIds[r] : r;
          this._devices[devR].counters.ncclOps++;
        }
        return 0;
      }

      const src = sendbufs[root];
      const bytesPerRank = count * 4;

      for (let r = 0; r < nranks; r++) {
        const dst = recvbufs[r];
        for (let i = 0; i < count; i++) {
          dst._rawSet(i, src._rawGet(i));
        }
        const devR = (comm && comm.deviceIds) ? comm.deviceIds[r] : r;
        if (nranks > 1 && r !== root) {
          this._devices[devR].counters.crossGpuBytes += bytesPerRank;
        }
        this._devices[devR].counters.ncclOps++;
      }
      return 0;
    }

    /**
     * ncclReduceScatter — reduce then scatter.
     * Each rank receives recvcount elements of the reduction.
     */
    ncclReduceScatter(sendbufs, recvbufs, recvcount, datatype, op, comm) {
      if (recvcount < 0) throw new Error('ncclInvalidArgument: recvcount must be non-negative');
      op = (typeof op === 'string' ? op.toLowerCase() : 'sum');

      // If called per-rank with a single buffer, stage until all ranks arrive
      if (!Array.isArray(sendbufs)) {
        const nranks = (comm && comm.nranks) ? comm.nranks : this._numDevices;
        const rank = (comm && comm.rank !== undefined) ? comm.rank : this._currentDevice;
        if (rank < 0 || rank >= nranks) throw new Error('ncclInvalidArgument: invalid rank ' + rank + ' for comm with ' + nranks + ' ranks');
        const clique = (comm && comm._clique) ? comm._clique : (this._defaultClique || (this._defaultClique = {
          nranks,
          pendingAllReduce: [],
          pendingBroadcast: [],
          pendingReduceScatter: [],
          pendingAllGather: [],
          pendingReduce: []
        }));
        this._trackCollective(comm, rank, nranks, 'reducescatter', recvcount, datatype, undefined, op);
        clique.pendingReduceScatter[rank] = { sendbuf: sendbufs, recvbuf: recvbufs, recvcount, datatype, op, comm };
        let ready = true;
        for (let r = 0; r < nranks; r++) {
          if (!clique.pendingReduceScatter[r]) { ready = false; break; }
        }
        if (ready) {
          const staged = clique.pendingReduceScatter;
          clique.pendingReduceScatter = [];
          const allSends = staged.map(s => s.sendbuf);
          const allRecvs = staged.map(s => s.recvbuf);
          return this.ncclReduceScatter(allSends, allRecvs, recvcount, datatype, op, comm || { nranks });
        }
        return 0;
      }

      const nranks = (comm && comm.nranks) ? comm.nranks : (Array.isArray(sendbufs) ? sendbufs.length : this._numDevices);
      if (sendbufs.length !== nranks) throw new Error('ncclInvalidArgument: sendbufs length (' + sendbufs.length + ') must match comm.nranks (' + nranks + ')');
      if (recvbufs.length !== nranks) throw new Error('ncclInvalidArgument: recvbufs length (' + recvbufs.length + ') must match comm.nranks (' + nranks + ')');

      if (recvcount === 0) {
        for (let r = 0; r < nranks; r++) {
          const devR = (comm && comm.deviceIds) ? comm.deviceIds[r] : r;
          this._devices[devR].counters.ncclOps++;
        }
        return 0;
      }

      const totalCount = recvcount * nranks;

      // Full reduce first
      const reduced = new Float32Array(totalCount);
      if (op === 'sum' || op === 'avg') reduced.fill(0);
      else if (op === 'prod') reduced.fill(1);
      else if (op === 'max') reduced.fill(-Infinity);
      else if (op === 'min') reduced.fill(Infinity);

      for (let r = 0; r < nranks; r++) {
        const src = sendbufs[r];
        for (let i = 0; i < totalCount; i++) {
          const val = src._rawGet(i);
          if (op === 'sum' || op === 'avg') reduced[i] += val;
          else if (op === 'prod') reduced[i] *= val;
          else if (op === 'max') reduced[i] = Math.max(reduced[i], val);
          else if (op === 'min') reduced[i] = Math.min(reduced[i], val);
        }
      }

      if (op === 'avg') {
        for (let i = 0; i < totalCount; i++) reduced[i] /= nranks;
      }

      // Scatter chunks
      for (let r = 0; r < nranks; r++) {
        const dst = recvbufs[r];
        const offset = r * recvcount;
        for (let i = 0; i < recvcount; i++) {
          dst._rawSet(i, reduced[offset + i]);
        }
        const devR = (comm && comm.deviceIds) ? comm.deviceIds[r] : r;
        if (nranks > 1) {
          const isRing = (comm && comm.algorithm === 'ring') || (this._collectiveAlgorithm === 'ring');
          if (isRing) {
            this._devices[devR].counters.crossGpuBytes += Math.round((nranks - 1) / nranks * (totalCount * 4));
          } else {
            this._devices[devR].counters.crossGpuBytes += recvcount * 4 * (nranks - 1);
          }
        }
        this._devices[devR].counters.ncclOps++;
      }
      return 0;
    }

    /**
     * ncclAllGather — gather data from all ranks to all ranks.
     * Each rank contributes sendcount elements; each receives nranks*sendcount.
     */
    ncclAllGather(sendbufs, recvbufs, sendcount, datatype, comm) {
      if (sendcount < 0) throw new Error('ncclInvalidArgument: count cannot be negative (sendcount = ' + sendcount + ')');

      // If called per-rank with a single buffer, stage until all ranks arrive
      if (!Array.isArray(sendbufs)) {
        const nranks = (comm && comm.nranks) ? comm.nranks : this._numDevices;
        const rank = (comm && comm.rank !== undefined) ? comm.rank : this._currentDevice;
        if (rank < 0 || rank >= nranks) throw new Error('ncclInvalidArgument: invalid rank ' + rank + ' for comm with ' + nranks + ' ranks');
        const clique = (comm && comm._clique) ? comm._clique : (this._defaultClique || (this._defaultClique = {
          nranks,
          pendingAllReduce: [],
          pendingBroadcast: [],
          pendingReduceScatter: [],
          pendingAllGather: [],
          pendingReduce: []
        }));
        this._trackCollective(comm, rank, nranks, 'allgather', sendcount, datatype, undefined, undefined);
        clique.pendingAllGather[rank] = { sendbuf: sendbufs, recvbuf: recvbufs, sendcount, datatype, comm };
        let ready = true;
        for (let r = 0; r < nranks; r++) {
          if (!clique.pendingAllGather[r]) { ready = false; break; }
        }
        if (ready) {
          const staged = clique.pendingAllGather;
          clique.pendingAllGather = [];
          const allSends = staged.map(s => s.sendbuf);
          const allRecvs = staged.map(s => s.recvbuf);
          return this.ncclAllGather(allSends, allRecvs, sendcount, datatype, comm || { nranks });
        }
        return 0;
      }

      const nranks = (comm && comm.nranks) ? comm.nranks : (Array.isArray(sendbufs) ? sendbufs.length : this._numDevices);
      if (sendbufs.length !== nranks) throw new Error('ncclInvalidArgument: sendbufs length (' + sendbufs.length + ') must match comm.nranks (' + nranks + ')');
      if (recvbufs.length !== nranks) throw new Error('ncclInvalidArgument: recvbufs length (' + recvbufs.length + ') must match comm.nranks (' + nranks + ')');

      if (sendcount === 0) {
        for (let r = 0; r < nranks; r++) {
          const devR = (comm && comm.deviceIds) ? comm.deviceIds[r] : r;
          this._devices[devR].counters.ncclOps++;
        }
        return 0;
      }

      for (let r = 0; r < nranks; r++) {
        const dst = recvbufs[r];
        for (let src_r = 0; src_r < nranks; src_r++) {
          const src = sendbufs[src_r];
          const dstOffset = src_r * sendcount;
          for (let i = 0; i < sendcount; i++) {
            dst._rawSet(dstOffset + i, src._rawGet(i));
          }
        }
        const devR = (comm && comm.deviceIds) ? comm.deviceIds[r] : r;
        if (nranks > 1) {
          this._devices[devR].counters.crossGpuBytes += sendcount * 4 * (nranks - 1);
        }
        this._devices[devR].counters.ncclOps++;
      }
      return 0;
    }

    /**
     * ncclReduce — reduce across devices into root rank buffer.
     */
    ncclReduce(sendbufs, recvbufs, count, datatype, op, root, comm) {
      if (count < 0) throw new Error('ncclInvalidArgument: count must be non-negative');
      op = (typeof op === 'string' ? op.toLowerCase() : 'sum');
      root = (typeof root === 'number' ? root : 0);
      const nranks = (comm && comm.nranks) ? comm.nranks : (Array.isArray(sendbufs) ? sendbufs.length : this._numDevices);
      if (root < 0 || root >= nranks) throw new Error('ncclInvalidArgument: invalid root ' + root);

      // If called per-rank with a single buffer, stage until all ranks arrive
      if (!Array.isArray(sendbufs)) {
        const rank = (comm && comm.rank !== undefined) ? comm.rank : this._currentDevice;
        if (rank < 0 || rank >= nranks) throw new Error('ncclInvalidArgument: invalid rank ' + rank);
        const clique = (comm && comm._clique) ? comm._clique : (this._defaultClique || (this._defaultClique = {
          nranks,
          pendingAllReduce: [],
          pendingBroadcast: [],
          pendingReduceScatter: [],
          pendingAllGather: [],
          pendingReduce: []
        }));
        if (!clique.pendingReduce) clique.pendingReduce = [];
        this._trackCollective(comm, rank, nranks, 'reduce', count, datatype, root, op);
        clique.pendingReduce[rank] = { sendbuf: sendbufs, recvbuf: recvbufs, count, datatype, op, root, comm };
        let ready = true;
        for (let r = 0; r < nranks; r++) {
          if (!clique.pendingReduce[r]) { ready = false; break; }
        }
        if (ready) {
          const staged = clique.pendingReduce;
          clique.pendingReduce = [];
          const allSends = staged.map(s => s.sendbuf);
          const allRecvs = staged.map(s => s.recvbuf);
          return this.ncclReduce(allSends, allRecvs, count, datatype, op, root, comm || { nranks });
        }
        return 0;
      }

      if (count === 0) {
        for (let r = 0; r < nranks; r++) {
          const dev = (comm && comm.deviceIds) ? comm.deviceIds[r] : r;
          this._devices[dev].counters.ncclOps++;
        }
        return 0;
      }

      const reduced = new Float32Array(count);
      if (op === 'sum' || op === 'avg') reduced.fill(0);
      else if (op === 'prod') reduced.fill(1);
      else if (op === 'max') reduced.fill(-Infinity);
      else if (op === 'min') reduced.fill(Infinity);

      for (let r = 0; r < nranks; r++) {
        const src = sendbufs[r];
        for (let i = 0; i < count; i++) {
          const val = src._rawGet(i);
          if (op === 'sum' || op === 'avg') reduced[i] += val;
          else if (op === 'prod') reduced[i] *= val;
          else if (op === 'max') reduced[i] = Math.max(reduced[i], val);
          else if (op === 'min') reduced[i] = Math.min(reduced[i], val);
        }
      }
      if (op === 'avg') {
        for (let i = 0; i < count; i++) reduced[i] /= nranks;
      }

      const dst = Array.isArray(recvbufs) ? recvbufs[root] : recvbufs;
      for (let i = 0; i < count; i++) {
        dst._rawSet(i, reduced[i]);
      }

      const bytesPerRank = count * 4;
      const rootDev = (comm && comm.deviceIds) ? comm.deviceIds[root] : root;
      this._devices[rootDev].counters.crossGpuBytes += bytesPerRank * (nranks - 1);
      for (let r = 0; r < nranks; r++) {
        const dev = (comm && comm.deviceIds) ? comm.deviceIds[r] : r;
        this._devices[dev].counters.ncclOps++;
      }
      return 0;
    }

    /**
     * ncclAllToAll — each rank sends countPerRank to every other rank.
     */
    ncclAllToAll(sendbufs, recvbufs, countPerRank, datatype, comm) {
      if (countPerRank < 0) throw new Error('ncclInvalidArgument: countPerRank must be non-negative');
      const nranks = (comm && comm.nranks) ? comm.nranks : (Array.isArray(sendbufs) ? sendbufs.length : this._numDevices);
      for (let r = 0; r < nranks; r++) {
        for (let q = 0; q < nranks; q++) {
          const srcOffset = q * countPerRank;
          const dstOffset = r * countPerRank;
          for (let i = 0; i < countPerRank; i++) {
            recvbufs[q]._rawSet(dstOffset + i, sendbufs[r]._rawGet(srcOffset + i));
          }
        }
      }
      for (let q = 0; q < nranks; q++) {
        const dev = (comm && comm.deviceIds) ? comm.deviceIds[q] : q;
        if (nranks > 1) {
          this._devices[dev].counters.crossGpuBytes += countPerRank * 4 * (nranks - 1);
        }
        this._devices[dev].counters.ncclOps++;
      }
      return 0;
    }

    /** Group semantics */
    ncclGroupStart() {
      this._groupDepth = (this._groupDepth || 0) + 1;
      if (this._groupDepth === 1) {
        this._groupP2POps = [];
      }
      return 0;
    }

    ncclGroupEnd() {
      if (!this._groupDepth || this._groupDepth <= 0) {
        throw new Error('ncclInvalidUsage: ncclGroupEnd called without matching ncclGroupStart');
      }
      this._groupDepth--;
      if (this._groupDepth === 0) {
        this._executeGroupedP2P();
      }
      return 0;
    }

    ncclSend(sendbuf, count, datatype, peer, comm) {
      if (count < 0) throw new Error('ncclInvalidArgument: count must be non-negative');
      const rank = (comm && comm.rank !== undefined) ? comm.rank : (sendbuf && sendbuf._deviceId !== undefined ? sendbuf._deviceId : this._currentDevice);
      const nranks = comm ? comm.nranks : this._numDevices;
      if (peer < 0 || peer >= nranks) throw new Error('ncclInvalidArgument: invalid peer ' + peer);
      const op = { type: 'send', rank, peer, buf: sendbuf, count, datatype, comm };
      if (this._groupDepth && this._groupDepth > 0) {
        this._groupP2POps.push(op);
      } else {
        this._stageOrExecuteP2P(op);
      }
      return 0;
    }

    ncclRecv(recvbuf, count, datatype, peer, comm) {
      if (count < 0) throw new Error('ncclInvalidArgument: count must be non-negative');
      const rank = (comm && comm.rank !== undefined) ? comm.rank : (recvbuf && recvbuf._deviceId !== undefined ? recvbuf._deviceId : this._currentDevice);
      const nranks = comm ? comm.nranks : this._numDevices;
      if (peer < 0 || peer >= nranks) throw new Error('ncclInvalidArgument: invalid peer ' + peer);
      const op = { type: 'recv', rank, peer, buf: recvbuf, count, datatype, comm };
      if (this._groupDepth && this._groupDepth > 0) {
        this._groupP2POps.push(op);
      } else {
        this._stageOrExecuteP2P(op);
      }
      return 0;
    }

    _stageOrExecuteP2P(op) {
      if (!this._stagedP2P) this._stagedP2P = [];
      this._stagedP2P.push(op);
    }

    _executeGroupedP2P() {
      const ops = this._groupP2POps || [];
      this._groupP2POps = [];
      const sends = ops.filter(o => o.type === 'send');
      const recvs = ops.filter(o => o.type === 'recv');

      for (const s of sends) {
        const matchingRecv = recvs.find(r => r.rank === s.peer && r.peer === s.rank);
        if (matchingRecv) {
          const count = Math.min(s.count, matchingRecv.count);
          for (let i = 0; i < count; i++) {
            matchingRecv.buf._rawSet(i, s.buf._rawGet(i));
          }
          const dstDev = (matchingRecv.comm && matchingRecv.comm.deviceIds) ? matchingRecv.comm.deviceIds[matchingRecv.rank] : matchingRecv.rank;
          this._devices[dstDev].counters.crossGpuBytes += count * 4;
          this._devices[dstDev].counters.ncclOps++;
        }
      }
    }

    setCollectiveAlgorithm(algo) {
      this._collectiveAlgorithm = algo;
    }

    getLeakReport() {
      const leaks = [];
      let totalLeakedBytes = 0;
      let totalAllocations = 0;
      for (let i = 0; i < this._devices.length; i++) {
        const mem = this._devices[i].memory;
        if (mem && mem._allocations) {
          for (const [allocId, alloc] of mem._allocations.entries()) {
            if (!alloc.ptr || !alloc.ptr._isFreed) {
              totalAllocations++;
              totalLeakedBytes += alloc.sizeBytes;
              leaks.push({
                deviceId: i,
                allocId,
                sizeBytes: alloc.sizeBytes,
                offset: alloc.offset !== undefined ? alloc.offset : 0
              });
            }
          }
        }
      }
      return { totalAllocations, totalLeakedBytes, leaks };
    }

    allReduce(sendbuf, recvbuf, count, datatype, op, comm) {
      return this.ncclAllReduce(sendbuf, recvbuf, count, datatype, op, comm);
    }

    get deviceCount() {
      return this._numDevices;
    }

    get numDevices() {
      return this._numDevices;
    }

    /**
     * Get per-device interface wrapper
     * @param {number} id
     */
    getDevice(id) {
      const dev = this._dev(id);
      return {
        cudaMalloc: (sizeBytes) => dev.memory.cudaMalloc(sizeBytes),
        cudaMemcpy: (dst, src, sizeBytes, kind) => {
          dev.memory.cudaMemcpy(dst, src, sizeBytes, kind);
          return 0;
        },
        cudaFree: (ptr) => {
          dev.memory.cudaFree(ptr);
          return 0;
        },
        counters: dev.counters,
        memory: dev.memory,
        launcher: dev.launcher
      };
    }

    /** Get counters for a specific device */
    getCounters(deviceId) {
      const idx = deviceId !== undefined ? deviceId : this._currentDevice;
      if (idx < 0 || idx >= this._numDevices) {
        throw new Error('Invalid device id: ' + idx);
      }
      return this._devices[idx].counters;
    }

    /** Get aggregated counters across all multi-GPU nodes */
    getAggregatedCounters() {
      const agg = new SimCounters(this._gpuProfile);
      for (let i = 0; i < this._numDevices; i++) {
        const c = this._devices[i].counters;
        c.flushWarpGlobalAccesses();
        c.flushSharedBankAccesses();
        agg.threadsLaunched += c.threadsLaunched;
        agg.blocksLaunched += c.blocksLaunched;
        agg.globalLoads += c.globalLoads;
        agg.globalStores += c.globalStores;
        agg.globalLoadBytes += c.globalLoadBytes;
        agg.globalStoreBytes += c.globalStoreBytes;
        agg.globalTransactions += c.globalTransactions;
        agg.sharedLoads += c.sharedLoads;
        agg.sharedStores += c.sharedStores;
        agg.sharedLoadBytes += c.sharedLoadBytes;
        agg.sharedStoreBytes += c.sharedStoreBytes;
        agg.bankConflicts += c.bankConflicts;
        agg.syncthreadsCount += c.syncthreadsCount;
        agg.divergentBranches += c.divergentBranches;
        agg.atomicOps += c.atomicOps;
        agg.atomicMaxContention = Math.max(agg.atomicMaxContention, c.atomicMaxContention);
        agg.memcpyH2DBytes += c.memcpyH2DBytes;
        agg.memcpyD2HBytes += c.memcpyD2HBytes;
        agg.crossGpuBytes += c.crossGpuBytes;
        agg.ncclOps += c.ncclOps;
        agg.flopCount += c.flopCount;
      }
      agg.perDevice = this._devices.map((d, idx) => ({
        deviceId: idx,
        ...d.counters.toJSON()
      }));
      return agg;
    }

    /** Reset all devices */
    reset() {
      for (let i = 0; i < this._devices.length; i++) {
        const dev = this._devices[i];
        dev.counters.reset();
        dev.launcher.clearDiagnostics();
        if (dev.memory) {
          dev.memory.destroy();
          dev.memory = new SimMemory(dev.counters, i);
        }
      }
      this._defaultClique = null;
      this._groupDepth = 0;
      this._groupP2POps = [];
      this._stagedP2P = [];
      if (this._desyncDetector) {
        this._desyncDetector.reset();
      }
      if (this._topologyModel) {
        this._topologyModel.reset();
      }
    }

    /** Destroy all devices */
    destroy() {
      for (const dev of this._devices) {
        dev.memory.destroy();
      }
    }
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // CudaRuntime — the main API that ties everything together
  // ═══════════════════════════════════════════════════════════════════════════

  class CudaRuntime {
    /**
     * @param {object} [gpuProfile] – GPU hardware profile for metric estimation.
     *   Fields: clockSpeedMHz, peakTFLOPS, peakGFLOPS, memBandwidthGBs,
     *           smCount, maxThreadsPerSM, globalMemLatencyCycles,
     *           sharedMemLatencyCycles, atomicLatencyCycles, syncLatencyCycles,
     *           flopLatencyCycles, maxSharedMemPerBlock, maxRegistersPerBlock
     */
    constructor(gpuProfile) {
      this._gpuProfile = gpuProfile || {
        clockSpeedMHz: 1500,
        peakTFLOPS: 19.5,
        peakGFLOPS: 19500,
        memBandwidthGBs: 900,
        smCount: 80,
        maxThreadsPerSM: 2048,
        globalMemLatencyCycles: 400,
        sharedMemLatencyCycles: 20,
        atomicLatencyCycles: 50,
        syncLatencyCycles: 5,
        flopLatencyCycles: 1,
        maxSharedMemPerBlock: 49152,
        maxRegistersPerBlock: 65536
      };

      this._counters = new SimCounters(this._gpuProfile);
      this._memory = new SimMemory(this._counters);
      this._launcher = new KernelLauncher(this._counters, this._gpuProfile);

      // Multi-GPU support
      this._multiGPU = null;
      this._currentDevice = 0;
    }

    // ── Memory API ──

    /**
     * Allocate device memory.
     * @param {number} sizeBytes
     * @returns {DevicePointer}
     */
    cudaMalloc(sizeBytes) {
      if (this._multiGPU) {
        return this._multiGPU.getDevice(this._currentDevice).cudaMalloc(sizeBytes);
      }
      return this._memory.cudaMalloc(sizeBytes);
    }

    /**
     * Free device memory.
     * @param {DevicePointer} ptr
     */
    cudaFree(ptr) {
      if (ptr && ptr._isFreed) {
        throw new Error('cudaErrorInvalidValue: double free or invalid pointer in cudaFree');
      }
      if (this._multiGPU) {
        return this._multiGPU.getDevice(this._currentDevice).cudaFree(ptr);
      }
      this._memory.cudaFree(ptr);
      return 0;
    }

    /**
     * Copy memory between host and device.
     * @param {DevicePointer|TypedArray} dst
     * @param {DevicePointer|TypedArray} src
     * @param {number} sizeBytes
     * @param {string} kind – 'H2D', 'D2H', 'D2D', 'H2H'
     */
    cudaMemcpy(dst, src, sizeBytes, kind) {
      if (this._multiGPU) {
        return this._multiGPU.getDevice(this._currentDevice).cudaMemcpy(dst, src, sizeBytes, kind);
      }
      this._memory.cudaMemcpy(dst, src, sizeBytes, kind);
      return 0;
    }

    /** Copy scalar float/int from device memory */
    cudaMemcpyD2H_Scalar(src, sizeBytes) {
      const bytes = (sizeBytes || 4);
      if (this._multiGPU) {
        this._multiGPU.getCounters(this._currentDevice).memcpyD2HBytes += bytes;
      } else {
        this._counters.memcpyD2HBytes += bytes;
      }
      return src && src._rawGet ? src._rawGet(0) : (src && src.get ? src.get(0) : (Array.isArray(src) || ArrayBuffer.isView(src) ? src[0] : src));
    }

    /** Copy scalar value into device memory */
    cudaMemcpyH2D_Scalar(dst, val, sizeBytes) {
      const bytes = (sizeBytes || 4);
      if (this._multiGPU) {
        this._multiGPU.getCounters(this._currentDevice).memcpyH2DBytes += bytes;
      } else {
        this._counters.memcpyH2DBytes += bytes;
      }
      const num = Number(val) || 0;
      if (dst && dst._rawSet) dst._rawSet(0, num);
      else if (dst && dst.set) dst.set(0, num);
      else if (Array.isArray(dst) || ArrayBuffer.isView(dst)) dst[0] = num;
    }

    /**
     * Set device memory.
     * @param {DevicePointer} ptr
     * @param {number} value
     * @param {number} sizeBytes
     */
    cudaMemset(ptr, value, sizeBytes) {
      if (this._multiGPU) {
        const mem = this._multiGPU.getDevice(this._currentDevice).memory;
        if (ptr && ptr._allocId) {
          const entry = mem._allocations.get(ptr._allocId);
          if (entry) {
            new Uint8Array(entry.buffer).fill(value & 0xFF, 0, Math.min(sizeBytes, entry.sizeBytes));
          }
        }
        return 0;
      }
      this._memory.cudaMemset(ptr, value, sizeBytes);
      return 0;
    }

    /** Synchronize device (no-op in simulation — all launches are sync) */
    cudaDeviceSynchronize() {
      return 0;
    }

    /**
     * Get the last error from kernel launch or runtime operation, and reset it.
     * Standard CUDA runtime semantics: returns error code and resets.
     */
    cudaGetLastError() {
      let err = null;
      if (this._launcher && this._launcher._lastError) {
        err = this._launcher._lastError;
        this._launcher._lastError = null;
      } else if (this._lastError) {
        err = this._lastError;
        this._lastError = null;
      } else if (this._multiGPU) {
        for (let d = 0; d < this._multiGPU.deviceCount; d++) {
          const l = this._multiGPU.getDevice(d).launcher;
          if (l && l._lastError) {
            err = l._lastError;
            l._lastError = null;
            break;
          }
        }
      }
      return err ? 1 /* cudaErrorLaunchFailure */ : 0 /* cudaSuccess */;
    }

    /**
     * Return the last error without resetting it.
     */
    cudaPeekAtLastError() {
      if (this._launcher && this._launcher._lastError) return 1;
      if (this._lastError) return 1;
      if (this._multiGPU) {
        for (let d = 0; d < this._multiGPU.deviceCount; d++) {
          const l = this._multiGPU.getDevice(d).launcher;
          if (l && l._lastError) return 1;
        }
      }
      return 0;
    }

    /**
     * Return descriptive string for an error code.
     */
    cudaGetErrorString(errCode) {
      if (!errCode || errCode === 0) return 'cudaSuccess';
      const last = (this._launcher && this._launcher._lastError) || this._lastError;
      if (last) return String(last);
      return 'cudaErrorLaunchFailure';
    }

    // ── Launch API ──

    /**
     * Launch a kernel.
     * @param {Function} kernelFn – Transpiled kernel function
     * @param {object|number|number[]} grid – Grid dimensions
     * @param {object|number|number[]} block – Block dimensions
     * @param {number} [sharedMem=0] – Dynamic shared memory bytes
     * @param {...*} args – Kernel arguments
     */
    launch(kernelFn, grid, block, sharedMem, ...args) {
      if (this._multiGPU) {
        this._multiGPU.getDevice(this._currentDevice).launcher.launch(kernelFn, grid, block, sharedMem || 0, ...args);
        return;
      }
      this._launcher.launch(kernelFn, grid, block, sharedMem || 0, ...args);
    }

    // ── Multi-GPU ──

    /**
     * Initialize multi-GPU support.
     * @param {number} numDevices
     */
    initMultiGPU(numDevices) {
      const n = Math.max(1, Number(numDevices) || 2);
      this._multiGPU = new MultiGPURuntime(n, this._gpuProfile);
      return this._multiGPU;
    }

    /** Set the active GPU device */
    setDevice(id) {
      const targetId = Number(id);
      if (Number.isNaN(targetId) || targetId < 0) {
        throw new Error('cudaErrorInvalidDevice: invalid device ordinal ' + id);
      }
      if (this._multiGPU) {
        if (targetId >= this._multiGPU.deviceCount) {
          throw new Error('cudaErrorInvalidDevice: invalid device ordinal ' + targetId + ' for cluster of size ' + this._multiGPU.deviceCount);
        }
        this._multiGPU.cudaSetDevice(targetId);
      } else if (targetId > 0) {
        this.initMultiGPU(Math.max(targetId + 1, 2));
        this._multiGPU.cudaSetDevice(targetId);
      }
      this._currentDevice = targetId;
      return 0;
    }

    /** Get the active GPU device */
    getDevice() {
      return this._currentDevice;
    }

    /** Get total device count */
    getDeviceCount() {
      if (this._multiGPU) return this._multiGPU.deviceCount;
      if (this.deviceCount && this.deviceCount > 1) return this.deviceCount;
      return (typeof window !== 'undefined' && window.clusterNodes) || this.deviceCount || 2;
    }

    /** Enable peer access to another device */
    cudaDeviceEnablePeerAccess(peerDevice, flags = 0) {
      if (!this._multiGPU) this.initMultiGPU(Math.max(peerDevice + 1, 2));
      return this._multiGPU.cudaDeviceEnablePeerAccess(peerDevice, flags);
    }

    /** Disable peer access to another device */
    cudaDeviceDisablePeerAccess(peerDevice) {
      if (this._multiGPU) return this._multiGPU.cudaDeviceDisablePeerAccess(peerDevice);
      return 0;
    }

    cudaSetDevice(id) {
      if (this._multiGPU) {
        this._multiGPU.cudaSetDevice(id);
      }
      this._currentDevice = id;
      return 0;
    }

    cudaGetDevice() {
      if (this._multiGPU) {
        return this._multiGPU.cudaGetDevice();
      }
      return this._currentDevice || 0;
    }

    cudaGetDeviceCount() {
      return this.getDeviceCount();
    }

    enablePeerAccess(peerId) {
      if (this._multiGPU) {
        this._multiGPU.cudaDeviceEnablePeerAccess(peerId, 0);
      }
      return 0;
    }

    /**
     * Copy between GPU devices.
     */
    memcpyPeer(dst, dstDev, src, srcDev, sizeBytes) {
      const maxDev = Math.max(Number(dstDev) || 0, Number(srcDev) || 0);
      if (!this._multiGPU || maxDev >= this._multiGPU.deviceCount) {
        this.initMultiGPU(Math.max(maxDev + 1, 2));
      }
      this._multiGPU.cudaMemcpyPeer(dst, dstDev, src, srcDev, sizeBytes);
      return 0;
    }

    ncclAllReduce(sendbuf, recvbuf, count, datatype, op, comm) {
      if (!this._multiGPU) {
        const nranks = (comm && comm.nranks) ? comm.nranks : 2;
        this.initMultiGPU(nranks);
      }
      return this._multiGPU.allReduce(sendbuf, recvbuf, count, datatype, op, comm);
    }

    // ── Query ──

    /** Get the current performance counters (aggregated across multi-GPU or for specific deviceId) */
    getCounters(deviceId) {
      if (this._multiGPU) {
        if (deviceId !== undefined) {
          return this._multiGPU.getCounters(deviceId);
        }
        return this._multiGPU.getAggregatedCounters();
      }
      this._counters.flushWarpGlobalAccesses();
      this._counters.flushSharedBankAccesses();
      return this._counters;
    }

    /** Get the GPU profile */
    getProfile() {
      return this._gpuProfile;
    }

    /** Get diagnostics from kernel execution */
    getDiagnostics() {
      if (this._multiGPU) {
        const seen = new Set();
        const all = [];
        const addDiag = (item, devId) => {
          if (!seen.has(item)) {
            seen.add(item);
            all.push(devId !== undefined && item.deviceId === undefined ? Object.assign({ deviceId: devId }, item) : item);
          }
        };

        for (const item of this._launcher.getDiagnostics()) {
          addDiag(item, this._currentDevice);
        }
        for (let d = 0; d < this._multiGPU.deviceCount; d++) {
          const devDiag = this._multiGPU.getDevice(d).launcher.getDiagnostics();
          for (const item of devDiag) {
            addDiag(item, d);
          }
        }
        return all;
      }
      return this._launcher.getDiagnostics();
    }

    /** Get the multi-GPU runtime (if initialized) */
    getMultiGPU() {
      return this._multiGPU;
    }

    // ── Lifecycle ──

    /** Print message from host code or kernel */
    printf(...args) {
      if (args.length === 0) return;
      let fmt = String(args[0]);
      let argIdx = 1;
      let formatted = fmt.replace(/%([0-9]*\.?[0-9]*[dfsuxXgG%])/g, (match, spec) => {
        if (spec === '%') return '%';
        if (argIdx >= args.length) return match;
        const val = args[argIdx++];
        if (spec.endsWith('f') || spec.endsWith('g') || spec.endsWith('G')) {
          const precision = spec.includes('.') ? parseInt(spec.split('.')[1]) : 6;
          return Number(val).toFixed(precision);
        }
        if (spec.endsWith('d') || spec.endsWith('i') || spec.endsWith('u')) {
          return parseInt(val, 10);
        }
        if (spec.endsWith('x') || spec.endsWith('X')) {
          return (val >>> 0).toString(16);
        }
        return String(val);
      });
      if (argIdx < args.length) {
        formatted += ' ' + args.slice(argIdx).join(' ');
      }
      const diagItem = {
        type: 'printf',
        message: formatted,
        block: { x: 0, y: 0, z: 0 },
        thread: { x: 0, y: 0, z: 0 },
        deviceId: this._currentDevice
      };
      this._launcher.getDiagnostics().push(diagItem);
      console.log('[CUDA printf]', formatted);
    }

    /** Multi-GPU NCCL Comm Init Rank */
    ncclCommInitRank(nranks, rank) {
      if (!this._multiGPU) this.initMultiGPU(nranks);
      return this._multiGPU.ncclCommInitRank(nranks, rank);
    }

    /** Multi-GPU NCCL Comm Init All */
    ncclCommInitAll(comms, nranks) {
      if (!this._multiGPU) this.initMultiGPU(nranks);
      return this._multiGPU.ncclCommInitAll(comms, nranks);
    }

    /** Multi-GPU NCCL AllReduce */
    ncclAllReduce(...args) {
      if (!this._multiGPU) this.initMultiGPU(this._numDevices || 2);
      return this._multiGPU.ncclAllReduce(...args);
    }

    /** Multi-GPU NCCL Broadcast */
    ncclBroadcast(...args) {
      if (!this._multiGPU) this.initMultiGPU(this._numDevices || 2);
      return this._multiGPU.ncclBroadcast(...args);
    }

    /** Multi-GPU NCCL ReduceScatter */
    ncclReduceScatter(...args) {
      if (!this._multiGPU) this.initMultiGPU(this._numDevices || 2);
      return this._multiGPU.ncclReduceScatter(...args);
    }

    /** Multi-GPU NCCL AllGather */
    ncclAllGather(...args) {
      if (!this._multiGPU) this.initMultiGPU(this._numDevices || 2);
      return this._multiGPU.ncclAllGather(...args);
    }

    /** Multi-GPU NCCL Reduce */
    ncclReduce(...args) {
      if (!this._multiGPU) this.initMultiGPU(this._numDevices || 2);
      return this._multiGPU.ncclReduce(...args);
    }

    /** Multi-GPU NCCL AllToAll */
    ncclAllToAll(...args) {
      if (!this._multiGPU) this.initMultiGPU(this._numDevices || 2);
      return this._multiGPU.ncclAllToAll(...args);
    }

    /** Multi-GPU NCCL Send */
    ncclSend(...args) {
      if (!this._multiGPU) this.initMultiGPU(this._numDevices || 2);
      return this._multiGPU.ncclSend(...args);
    }

    /** Multi-GPU NCCL Recv */
    ncclRecv(...args) {
      if (!this._multiGPU) this.initMultiGPU(this._numDevices || 2);
      return this._multiGPU.ncclRecv(...args);
    }

    /** Multi-GPU NCCL GroupStart */
    ncclGroupStart(...args) {
      if (!this._multiGPU) this.initMultiGPU(this._numDevices || 2);
      return this._multiGPU.ncclGroupStart(...args);
    }

    /** Multi-GPU NCCL GroupEnd */
    ncclGroupEnd(...args) {
      if (!this._multiGPU) this.initMultiGPU(this._numDevices || 2);
      return this._multiGPU.ncclGroupEnd(...args);
    }

    /** Get unfreed device memory allocations */
    getLeakReport() {
      if (this._multiGPU) return this._multiGPU.getLeakReport();
      const leaks = [];
      let totalLeakedBytes = 0;
      let totalAllocations = 0;
      if (this._memory && this._memory._allocations) {
        for (const [allocId, alloc] of this._memory._allocations.entries()) {
          if (!alloc.ptr || !alloc.ptr._isFreed) {
            totalAllocations++;
            totalLeakedBytes += alloc.sizeBytes;
            leaks.push({ allocId, sizeBytes: alloc.sizeBytes, offset: alloc.offset !== undefined ? alloc.offset : 0 });
          }
        }
      }
      return { totalAllocations, totalLeakedBytes, leaks };
    }

    /** Reset all counters and diagnostics across all devices */
    reset() {
      this._counters.reset();
      this._lastError = null;
      this._launcher.clearDiagnostics();
      if (this._memory) {
        this._memory.destroy();
        this._memory = new SimMemory(this._counters, 0);
      }
      if (this._multiGPU) {
        this._multiGPU.reset();
      }
    }

    /** Destroy the runtime and free all memory */
    destroy() {
      this._memory.destroy();
      if (this._multiGPU) {
        this._multiGPU.destroy();
        this._multiGPU = null;
      }
    }
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // Export everything on _g.CudaRuntime
  // ═══════════════════════════════════════════════════════════════════════════

  const _g = typeof window !== 'undefined' ? window : (typeof globalThis !== 'undefined' ? globalThis : global);

  _g.CudaRuntime = CudaRuntime;

  // Also export sub-classes and utilities for advanced use
  _g.CudaRuntime.DevicePointer = DevicePointer;
  _g.CudaRuntime.SimMemory = SimMemory;
  _g.CudaRuntime.SharedMemory = SharedMemory;
  _g.CudaRuntime.SimCounters = SimCounters;
  _g.CudaRuntime.KernelLauncher = KernelLauncher;
  _g.CudaRuntime.MultiGPURuntime = MultiGPURuntime;
  _g.CudaRuntime.NcclComm = NcclComm;
  _g.CudaRuntime.WarpState = WarpState;

  // Export standalone functions
  _g.CudaRuntime.atomicAdd = atomicAdd;
  _g.CudaRuntime.atomicSub = atomicSub;
  _g.CudaRuntime.atomicMax = atomicMax;
  _g.CudaRuntime.atomicMin = atomicMin;
  _g.CudaRuntime.atomicCAS = atomicCAS;
  _g.CudaRuntime.atomicExch = atomicExch;
  _g.CudaRuntime.atomicAnd = atomicAnd;
  _g.CudaRuntime.atomicOr = atomicOr;
  _g.CudaRuntime.atomicXor = atomicXor;

  // Warp intrinsics
  _g.CudaRuntime.__shfl_down_sync = __shfl_down_sync;
  _g.CudaRuntime.__shfl_up_sync = __shfl_up_sync;
  _g.CudaRuntime.__shfl_xor_sync = __shfl_xor_sync;
  _g.CudaRuntime.__shfl_sync = __shfl_sync;
  _g.CudaRuntime.__ballot_sync = __ballot_sync;
  _g.CudaRuntime.__all_sync = __all_sync;
  _g.CudaRuntime.__any_sync = __any_sync;
  _g.CudaRuntime.__popc = __popc;
  _g.CudaRuntime.__clz = __clz;

  // ═══════════════════════════════════════════════════════════════════════════
  // InferenceCluster — Multi-GPU LLM Inference & Traffic Overload Simulator
  // ═══════════════════════════════════════════════════════════════════════════

  class InferenceCluster {
    /**
     * @param {object} [config]
     */
    constructor(config = {}) {
      this.gpuModel = config.gpuModel || 'A100-SXM4-80GB';
      this.gpuCount = config.gpuCount || 8;
      this.tensorParallel = config.tensorParallel || Math.min(8, this.gpuCount);
      this.pipelineParallel = config.pipelineParallel || Math.max(1, Math.floor(this.gpuCount / this.tensorParallel));
      this.dataParallelReplicas = Math.max(1, Math.floor(this.gpuCount / (this.tensorParallel * this.pipelineParallel)));
      this.modelParamsB = config.modelParamsB || 70;
      this.kvCacheDtypeBytes = config.kvCacheDtypeBytes || 2;
      this.gpuVramGB = config.gpuVramGB || (this.gpuModel.includes('4090') ? 24 : 80);
      this.peakTFLOPS = config.peakTFLOPS || (this.gpuModel.includes('H100') ? 989 : (this.gpuModel.includes('A100') ? 312 : 82.6));
      this.memBandwidthGBs = config.memBandwidthGBs || (this.gpuModel.includes('H100') ? 3350 : (this.gpuModel.includes('A100') ? 2039 : 1008));
      this.interconnectBandwidthGBs = config.interconnectBandwidthGBs || (this.gpuModel.includes('H100') ? 900 : (this.gpuModel.includes('A100') ? 600 : 64));
      this.numLayers = config.numLayers || (this.modelParamsB >= 70 ? 80 : 32);
      this.hiddenSize = config.hiddenSize || (this.modelParamsB >= 70 ? 8192 : 4096);
      this.numHeads = config.numHeads || (this.modelParamsB >= 70 ? 64 : 32);
      this.numKvHeads = config.numKvHeads || (this.modelParamsB >= 70 ? 8 : 8);

      // Memory breakdown
      const totalWeightGB = this.modelParamsB * 2;
      this.weightPerGpuGB = totalWeightGB / (this.tensorParallel * this.pipelineParallel);
      this.systemReserveGB = 4.0;
      this.availableKvCacheGBPerGpu = Math.max(0, this.gpuVramGB - this.weightPerGpuGB - this.systemReserveGB);

      // KV cache bytes per token across all layers
      const kvDim = (this.hiddenSize * this.numKvHeads) / this.numHeads;
      this.kvBytesPerTokenTotal = 2 * this.numLayers * kvDim * this.kvCacheDtypeBytes;
      this.kvBytesPerTokenPerGpu = this.kvBytesPerTokenTotal / this.tensorParallel;

      // Max concurrent tokens across cluster
      this.maxConcurrentTokensPerGpu = Math.floor((this.availableKvCacheGBPerGpu * 1024 * 1024 * 1024) / Math.max(1, this.kvBytesPerTokenPerGpu));
      this.maxConcurrentTokensCluster = this.maxConcurrentTokensPerGpu * this.tensorParallel * this.dataParallelReplicas;
    }

    /**
     * Compute single request baseline latencies (uncongested)
     */
    estimateRequestLatencies(promptLen = 512, genLen = 128) {
      // 1. TTFT (Prefill Phase):
      const prefillFlops = 2 * (this.modelParamsB * 1e9) * promptLen;
      const clusterComputeTFLOPS = this.tensorParallel * this.pipelineParallel * this.peakTFLOPS * 1e12;
      const tPrefillComputeMs = (prefillFlops / clusterComputeTFLOPS) * 1000 * 2.2; // 45% MFU

      // NVLink TP AllReduce comm per layer
      const commBytesPrefillLayer = 2 * ((this.tensorParallel - 1) / this.tensorParallel) * (promptLen * this.hiddenSize * 2);
      const totalCommBytesPrefill = commBytesPrefillLayer * this.numLayers * 2;
      const tPrefillCommMs = (totalCommBytesPrefill / (this.interconnectBandwidthGBs * 1e9)) * 1000;

      const ttftMs = Math.max(1.5, tPrefillComputeMs + tPrefillCommMs);

      // 2. ITL (Decode Phase per token):
      const tReadWeightsMs = ((this.weightPerGpuGB * 1e9) / (this.memBandwidthGBs * 1e9)) * 1000;
      const commBytesDecodeStep = 2 * ((this.tensorParallel - 1) / this.tensorParallel) * (1 * this.hiddenSize * 2) * this.numLayers * 2;
      const tDecodeCommMs = (commBytesDecodeStep / (this.interconnectBandwidthGBs * 1e9)) * 1000;

      const itlMs = Math.max(0.8, tReadWeightsMs + tDecodeCommMs);
      const totalGenTimeMs = ttftMs + (genLen * itlMs);

      return {
        ttftMs: Number(ttftMs.toFixed(2)),
        itlMs: Number(itlMs.toFixed(2)),
        totalGenTimeMs: Number(totalGenTimeMs.toFixed(2)),
        tPrefillComputeMs: Number(tPrefillComputeMs.toFixed(2)),
        tPrefillCommMs: Number(tPrefillCommMs.toFixed(2)),
        tDecodeCommMs: Number(tDecodeCommMs.toFixed(2))
      };
    }

    /**
     * Simulate cluster performance under traffic load & burst spikes.
     */
    simulateTraffic(workload = {}) {
      const targetRps = workload.targetRps || 50;
      const durationSec = workload.durationSec || 10;
      const burstMultiplier = workload.burstMultiplier || 1.0;
      const avgPromptLen = workload.avgPromptLen || 512;
      const avgGenLen = workload.avgGenLen || 128;
      const totalTokensPerReq = avgPromptLen + avgGenLen;

      const base = this.estimateRequestLatencies(avgPromptLen, avgGenLen);
      const peakRps = targetRps * burstMultiplier;
      const totalRequests = Math.round(peakRps * durationSec);
      const maxConcurrentRequests = Math.max(1, Math.floor(this.maxConcurrentTokensCluster / totalTokensPerReq));
      const maxBatchSize = workload.maxBatchSize || 256;
      const effectiveMaxConcurrent = Math.min(maxConcurrentRequests, maxBatchSize * this.dataParallelReplicas);

      const queueDepthHistory = [];
      const kvSaturationHistory = [];
      let currentActiveRequests = 0;
      let currentQueueDepth = 0;
      let droppedRequests = 0;
      let servedRequests = 0;
      let partialCompleted = 0.0;
      const latencies = [];

      const timeSteps = 50;
      const dt = durationSec / timeSteps;
      const reqsPerSlice = (peakRps * dt);

      for (let step = 0; step < timeSteps; step++) {
        const arriving = Math.round(reqsPerSlice * (0.9 + Math.random() * 0.2));

        for (let i = 0; i < arriving; i++) {
          if (currentActiveRequests < effectiveMaxConcurrent) {
            currentActiveRequests++;
          } else {
            if (currentQueueDepth < effectiveMaxConcurrent * 2) {
              currentQueueDepth++;
            } else {
              droppedRequests++;
            }
          }
        }

        const currentBatch = Math.max(1, currentActiveRequests);
        const batchDecodeStepMs = base.itlMs + (currentBatch * 0.012);
        const tokensGeneratedSlice = (currentActiveRequests * ((dt * 1000) / batchDecodeStepMs));
        const requestsCompletedFraction = tokensGeneratedSlice / avgGenLen;
        partialCompleted += requestsCompletedFraction;

        const completed = Math.min(currentActiveRequests, Math.floor(partialCompleted));
        partialCompleted -= completed;
        currentActiveRequests -= completed;
        servedRequests += completed;

        const slotsAvailable = effectiveMaxConcurrent - currentActiveRequests;
        const admittedFromQueue = Math.min(currentQueueDepth, slotsAvailable);
        currentQueueDepth -= admittedFromQueue;
        currentActiveRequests += admittedFromQueue;

        const currentActiveTokens = (currentActiveRequests * totalTokensPerReq);
        const kvSaturationPct = Math.min(100, (currentActiveTokens / this.maxConcurrentTokensCluster) * 100);

        queueDepthHistory.push(currentQueueDepth);
        kvSaturationHistory.push(Number(kvSaturationPct.toFixed(1)));

        const batchDegradation = 1.0 + Math.pow(kvSaturationPct / 100, 2) * 1.5;
        const queueWaitTimeMs = (currentQueueDepth / Math.max(1, peakRps)) * 1000;
        const effectiveTtftMs = base.ttftMs * (1.0 + currentQueueDepth * 0.04) + queueWaitTimeMs;
        const effectiveItlMs = batchDecodeStepMs * batchDegradation;
        const totalLatencyMs = effectiveTtftMs + (avgGenLen * effectiveItlMs);

        for (let k = 0; k < completed; k++) {
          const jitter = (Math.random() - 0.5) * 0.12 * totalLatencyMs;
          latencies.push(Math.max(base.totalGenTimeMs, totalLatencyMs + jitter));
        }
      }

      while (latencies.length < servedRequests) {
        latencies.push(base.totalGenTimeMs * (1.0 + (queueDepthHistory[queueDepthHistory.length - 1] / Math.max(1, peakRps))));
      }

      latencies.sort((a, b) => a - b);
      const p50 = latencies[Math.floor(latencies.length * 0.50)] || base.totalGenTimeMs;
      const p90 = latencies[Math.floor(latencies.length * 0.90)] || (base.totalGenTimeMs * 1.5);
      const p95 = latencies[Math.floor(latencies.length * 0.95)] || (base.totalGenTimeMs * 2.0);
      const p99 = latencies[Math.floor(latencies.length * 0.99)] || (base.totalGenTimeMs * 3.5);

      const maxQueueDepth = Math.max(...queueDepthHistory, 0);
      const peakKvSaturationPct = Math.max(...kvSaturationHistory, 0);
      const totalTokensGenerated = servedRequests * avgGenLen;
      const tokenThroughputTps = totalTokensGenerated / durationSec;

      return {
        clusterConfig: {
          gpuModel: this.gpuModel,
          gpuCount: this.gpuCount,
          tensorParallel: this.tensorParallel,
          pipelineParallel: this.pipelineParallel,
          dataParallelReplicas: this.dataParallelReplicas,
          modelParamsB: this.modelParamsB,
          weightPerGpuGB: Number(this.weightPerGpuGB.toFixed(2)),
          availableKvCacheGBPerGpu: Number(this.availableKvCacheGBPerGpu.toFixed(2)),
          maxConcurrentTokensCluster: this.maxConcurrentTokensCluster,
          maxConcurrentRequests: maxConcurrentRequests
        },
        trafficMetrics: {
          targetRps,
          burstMultiplier,
          peakRps,
          durationSec,
          totalArrivedRequests: totalRequests,
          servedRequests,
          droppedRequests,
          dropRatePct: Number(((droppedRequests / Math.max(1, totalRequests)) * 100).toFixed(2)),
          tokenThroughputTps: Number(tokenThroughputTps.toFixed(1))
        },
        baselineLatency: base,
        congestedLatency: {
          p50Ms: Number(p50.toFixed(2)),
          p90Ms: Number(p90.toFixed(2)),
          p95Ms: Number(p95.toFixed(2)),
          p99Ms: Number(p99.toFixed(2)),
          maxQueueDepth,
          peakKvSaturationPct
        },
        history: {
          queueDepth: queueDepthHistory,
          kvSaturationPct: kvSaturationHistory
        }
      };
    }
  }

  // Math context builder
  _g.CudaRuntime.buildMathContext = buildMathContext;
  _g.CudaRuntime.InferenceCluster = InferenceCluster;
  _g.InferenceCluster = InferenceCluster;

  // Helpers
  _g.CudaRuntime.dim3 = dim3;

  // Memory copy constants
  _g.CudaRuntime.cudaMemcpyHostToDevice = CUDA_MEMCPY_H2D;
  _g.CudaRuntime.cudaMemcpyDeviceToHost = CUDA_MEMCPY_D2H;
  _g.CudaRuntime.cudaMemcpyDeviceToDevice = CUDA_MEMCPY_D2D;
  _g.CudaRuntime.cudaMemcpyHostToHost = CUDA_MEMCPY_H2H;

  // Constants
  _g.CudaRuntime.WARP_SIZE = WARP_SIZE;

  // Register standard C math helpers globally for bare calls in generated code
  if (_g) {
    _g.isinf = function (x) { return !Number.isFinite(x) && !Number.isNaN(x); };
    _g.isinff = _g.isinf;
    _g.__isinf = _g.isinf;
    _g.__isinff = _g.isinf;
    _g.isnan = Number.isNaN;
    _g.isnanf = Number.isNaN;
    _g.__isnan = Number.isNaN;
    _g.__isnanf = Number.isNaN;
    _g.isfinite = Number.isFinite;
    _g.isfinitef = Number.isFinite;
    _g.__finite = Number.isFinite;
    _g.__finitef = Number.isFinite;
    _g.signbit = function (x) { return Math.sign(x) < 0 || Object.is(x, -0); };
    _g.signbitf = _g.signbit;
    _g.rsqrtf = function (x) { return 1.0 / Math.sqrt(x); };
    _g.rsqrt = _g.rsqrtf;
    _g.__rsqrtf = _g.rsqrtf;
    _g.fmaxf = Math.max;
    _g.fmax = Math.max;
    _g.fminf = Math.min;
    _g.fmin = Math.min;
    _g.fabsf = Math.abs;
    _g.fabs = Math.abs;
    _g.copysign = function (mag, sgn) { return Math.sign(sgn) === 0 ? Math.abs(mag) : Math.abs(mag) * Math.sign(sgn); };
    _g.copysignf = _g.copysign;
    _g.fmaf = function (a, b, c) { return Math.fround(a * b + c); };
    _g.fma = function (a, b, c) { return a * b + c; };

    // CUDA & NCCL return codes and enum constants
    _g.cudaSuccess = 0;
    _g.ncclSuccess = 0;
    _g.ncclFloat = 'float32';
    _g.ncclFloat32 = 'float32';
    _g.ncclHalf = 'float16';
    _g.ncclFloat16 = 'float16';
    _g.ncclInt = 'int32';
    _g.ncclInt32 = 'int32';
    _g.ncclSum = 'sum';
    _g.ncclProd = 'prod';
    _g.ncclMax = 'max';
    _g.ncclMin = 'min';
    _g.ncclAvg = 'avg';
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
      CudaRuntime,
      DevicePointer,
      SimMemory,
      SharedMemory,
      SimCounters,
      KernelLauncher,
      MultiGPURuntime,
      MultiGPUSimulator: MultiGPURuntime,
      NcclComm,
      NCCLCommunicator: NcclComm,
      InferenceCluster,
      buildMathContext,
      dim3
    };
  }

})();
