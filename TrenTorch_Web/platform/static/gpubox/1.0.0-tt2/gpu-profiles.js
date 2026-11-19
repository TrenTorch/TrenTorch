/**
 * GPU Hardware Profiles for CUDA Simulator
 *
 * Contains accurate real-world specifications for NVIDIA GPUs used to model
 * execution timing, resource limits, and hardware behavior in the simulator.
 *
 * Sources: Official NVIDIA datasheets, architecture whitepapers, and
 * techpowerup.com GPU database.
 */
(function () {
  'use strict';

  var profiles = {

    // =========================================================================
    // NVIDIA A100 80GB SXM — Ampere Data Center GPU (GA100)
    // =========================================================================
    'A100': {
      name: 'NVIDIA A100 80GB SXM',
      architecture: 'Ampere',
      computeCapability: '8.0',

      // Streaming Multiprocessors
      smCount: 108,
      maxThreadsPerSM: 2048,
      maxThreadsPerBlock: 1024,
      maxBlocksPerSM: 32,
      warpSize: 32,

      // Memory
      globalMemoryGB: 80,
      sharedMemoryPerSMKB: 164,       // max configurable shared memory per SM
      sharedMemoryPerBlockKB: 48,     // default shared memory per block
      l2CacheMB: 40,
      registerFilePerSMKB: 256,       // 65536 x 32-bit registers = 256 KB

      // Bandwidth
      memoryBandwidthGBs: 2039,       // HBM2e peak bandwidth
      l2BandwidthGBs: 4000,           // approximate aggregate L2 bandwidth
      sharedMemBandwidthGBs: 19000,   // approximate aggregate across all SMs

      // Clock
      baseClockMHz: 1095,
      boostClockMHz: 1410,
      memoryClockMHz: 1215,           // HBM2e actual clock (2430 MHz effective)

      // Interconnect
      nvlinkBandwidthGBs: 600,        // total bidirectional NVLink bandwidth
      nvlinkConnections: 12,          // NVLink 3.0 links
      pcieGen: 4,
      pcieLanes: 16,
      pcieBandwidthGBs: 31.5,

      // Compute
      fp32CoresPerSM: 64,
      fp64CoresPerSM: 32,
      tensorCoresPerSM: 4,            // 3rd gen Tensor Cores
      fp32TFLOPS: 19.5,
      fp16TFLOPS: 312,                // with sparsity
      fp64TFLOPS: 9.7,

      // Shared memory bank configuration
      sharedMemBanks: 32,
      sharedMemBankWidthBytes: 4,

      // Execution limits
      maxGridDimX: 2147483647,
      maxGridDimY: 65535,
      maxGridDimZ: 65535,
      maxBlockDimX: 1024,
      maxBlockDimY: 1024,
      maxBlockDimZ: 64,
      maxRegistersPerThread: 255,
      maxRegistersPerBlock: 65536,

      // Cache line sizes
      globalCacheLineSizeBytes: 128,   // L1 cache line = 128 bytes
      sectorSizeBytes: 32,            // memory sector = 32 bytes

      // Latencies (approximate cycles)
      globalMemLatencyCycles: 290,
      sharedMemLatencyCycles: 23,
      l2CacheLatencyCycles: 193,
      arithmeticLatencyCycles: 4,
      syncthreadsLatencyCycles: 16
    },

    // =========================================================================
    // NVIDIA H100 80GB SXM — Hopper Data Center GPU (GH100)
    // =========================================================================
    'H100': {
      name: 'NVIDIA H100 80GB SXM',
      architecture: 'Hopper',
      computeCapability: '9.0',

      // Streaming Multiprocessors
      smCount: 132,
      maxThreadsPerSM: 2048,
      maxThreadsPerBlock: 1024,
      maxBlocksPerSM: 32,
      warpSize: 32,

      // Memory
      globalMemoryGB: 80,
      sharedMemoryPerSMKB: 228,       // max configurable shared memory per SM
      sharedMemoryPerBlockKB: 48,     // default shared memory per block
      l2CacheMB: 50,
      registerFilePerSMKB: 256,       // 65536 x 32-bit registers = 256 KB

      // Bandwidth
      memoryBandwidthGBs: 3350,       // HBM3 peak bandwidth (3.35 TB/s)
      l2BandwidthGBs: 6000,           // approximate aggregate L2 bandwidth
      sharedMemBandwidthGBs: 33000,   // approximate aggregate across all SMs

      // Clock
      baseClockMHz: 1593,
      boostClockMHz: 1980,
      memoryClockMHz: 2619,           // HBM3 clock

      // Interconnect
      nvlinkBandwidthGBs: 900,        // total bidirectional NVLink 4.0 bandwidth
      nvlinkConnections: 18,          // NVLink 4.0 links
      pcieGen: 5,
      pcieLanes: 16,
      pcieBandwidthGBs: 63.0,         // PCIe Gen5 x16

      // Compute
      fp32CoresPerSM: 128,
      fp64CoresPerSM: 64,
      tensorCoresPerSM: 4,            // 4th gen Tensor Cores
      fp32TFLOPS: 67.0,
      fp16TFLOPS: 1979,               // with sparsity
      fp64TFLOPS: 34.0,

      // Shared memory bank configuration
      sharedMemBanks: 32,
      sharedMemBankWidthBytes: 4,

      // Execution limits
      maxGridDimX: 2147483647,
      maxGridDimY: 65535,
      maxGridDimZ: 65535,
      maxBlockDimX: 1024,
      maxBlockDimY: 1024,
      maxBlockDimZ: 64,
      maxRegistersPerThread: 255,
      maxRegistersPerBlock: 65536,

      // Cache line sizes
      globalCacheLineSizeBytes: 128,
      sectorSizeBytes: 32,

      // Latencies (approximate cycles — Hopper has lower latency than Ampere)
      globalMemLatencyCycles: 220,
      sharedMemLatencyCycles: 20,
      l2CacheLatencyCycles: 150,
      arithmeticLatencyCycles: 4,
      syncthreadsLatencyCycles: 12
    },

    // =========================================================================
    // NVIDIA GeForce RTX 4090 — Ada Lovelace Consumer Flagship (AD102)
    // =========================================================================
    'RTX 4090': {
      name: 'NVIDIA GeForce RTX 4090',
      architecture: 'Ada Lovelace',
      computeCapability: '8.9',

      // Streaming Multiprocessors
      smCount: 128,
      maxThreadsPerSM: 1536,
      maxThreadsPerBlock: 1024,
      maxBlocksPerSM: 24,
      warpSize: 32,

      // Memory
      globalMemoryGB: 24,
      sharedMemoryPerSMKB: 100,       // max configurable shared memory per SM
      sharedMemoryPerBlockKB: 48,     // default shared memory per block
      l2CacheMB: 72,
      registerFilePerSMKB: 256,       // 65536 x 32-bit registers = 256 KB

      // Bandwidth
      memoryBandwidthGBs: 1008,       // GDDR6X 384-bit @ 21 Gbps
      l2BandwidthGBs: 5000,           // approximate — large L2 cache
      sharedMemBandwidthGBs: 18000,   // approximate aggregate across all SMs

      // Clock
      baseClockMHz: 2235,
      boostClockMHz: 2520,
      memoryClockMHz: 1313,           // GDDR6X actual clock (21 Gbps effective)

      // Interconnect (no NVLink on consumer Ada)
      nvlinkBandwidthGBs: 0,
      nvlinkConnections: 0,
      pcieGen: 4,
      pcieLanes: 16,
      pcieBandwidthGBs: 31.5,

      // Compute
      fp32CoresPerSM: 128,
      fp64CoresPerSM: 2,              // Ada has 1:64 FP64:FP32 ratio
      tensorCoresPerSM: 4,            // 4th gen Tensor Cores
      fp32TFLOPS: 82.6,
      fp16TFLOPS: 330.3,              // with sparsity (Tensor)
      fp64TFLOPS: 1.29,               // very limited FP64 on consumer

      // Shared memory bank configuration
      sharedMemBanks: 32,
      sharedMemBankWidthBytes: 4,

      // Execution limits
      maxGridDimX: 2147483647,
      maxGridDimY: 65535,
      maxGridDimZ: 65535,
      maxBlockDimX: 1024,
      maxBlockDimY: 1024,
      maxBlockDimZ: 64,
      maxRegistersPerThread: 255,
      maxRegistersPerBlock: 65536,

      // Cache line sizes
      globalCacheLineSizeBytes: 128,
      sectorSizeBytes: 32,

      // Latencies (approximate cycles)
      globalMemLatencyCycles: 290,
      sharedMemLatencyCycles: 22,
      l2CacheLatencyCycles: 160,
      arithmeticLatencyCycles: 4,
      syncthreadsLatencyCycles: 16
    },

    // =========================================================================
    // NVIDIA GeForce RTX 5060 Ti — Blackwell Mid-Range Consumer (GB206)
    // =========================================================================
    'RTX 5060 Ti': {
      name: 'NVIDIA GeForce RTX 5060 Ti',
      architecture: 'Blackwell',
      computeCapability: '12.0 (TO VERIFY)',
      verificationStatus: 'TO VERIFY (Projected / Unreleased)',

      // Streaming Multiprocessors
      smCount: 36,
      maxThreadsPerSM: 1536,
      maxThreadsPerBlock: 1024,
      maxBlocksPerSM: 24,
      warpSize: 32,

      // Memory
      globalMemoryGB: 16,
      sharedMemoryPerSMKB: 100,       // 128 KB combined L1/shared, up to 100 KB shared
      sharedMemoryPerBlockKB: 48,     // default shared memory per block
      l2CacheMB: 32,
      registerFilePerSMKB: 256,       // 65536 x 32-bit registers = 256 KB

      // Bandwidth
      memoryBandwidthGBs: 448,        // GDDR7 128-bit @ 28 Gbps
      memBandwidthGBs: 448,
      l2BandwidthGBs: 2000,           // approximate
      sharedMemBandwidthGBs: 5000,    // approximate aggregate across all SMs

      // Clock
      baseClockMHz: 2407,
      boostClockMHz: 2572,
      memoryClockMHz: 1750,           // GDDR7 actual clock (28 Gbps effective)

      // Interconnect (no NVLink on consumer Blackwell)
      nvlinkBandwidthGBs: 0,
      nvlinkConnections: 0,
      pcieGen: 5,
      pcieLanes: 8,                   // PCIe 5.0 x8
      pcieBandwidthGBs: 31.5,         // PCIe 5.0 x8 ≈ PCIe 4.0 x16

      // Compute
      fp32CoresPerSM: 128,
      fp64CoresPerSM: 2,              // limited FP64 on consumer Blackwell
      tensorCoresPerSM: 4,            // 5th gen Tensor Cores
      fp32TFLOPS: 23.7,
      fp16TFLOPS: 189.6,              // with sparsity (Tensor FP8/INT8 class)
      fp64TFLOPS: 0.37,               // very limited FP64 on consumer

      // Shared memory bank configuration
      sharedMemBanks: 32,
      sharedMemBankWidthBytes: 4,

      // Execution limits
      maxGridDimX: 2147483647,
      maxGridDimY: 65535,
      maxGridDimZ: 65535,
      maxBlockDimX: 1024,
      maxBlockDimY: 1024,
      maxBlockDimZ: 64,
      maxRegistersPerThread: 255,
      maxRegistersPerBlock: 65536,

      // Cache line sizes
      globalCacheLineSizeBytes: 128,
      sectorSizeBytes: 32,

      // Latencies (approximate cycles — Blackwell has improved latency)
      globalMemLatencyCycles: 260,
      sharedMemLatencyCycles: 20,
      l2CacheLatencyCycles: 140,
      arithmeticLatencyCycles: 4,
      syncthreadsLatencyCycles: 12
    },

    // =========================================================================
    // NVIDIA GeForce RTX 4050 Laptop GPU — Ada Lovelace (AD107)
    // =========================================================================
    'RTX 4050 Laptop': {
      name: 'NVIDIA GeForce RTX 4050 Laptop GPU',
      architecture: 'Ada Lovelace',
      computeCapability: '8.9',
      verificationStatus: 'VERIFIED_PHYSICAL_HARDWARE',

      // Streaming Multiprocessors
      smCount: 20,
      maxThreadsPerSM: 1536,
      maxThreadsPerBlock: 1024,
      maxBlocksPerSM: 24,
      warpSize: 32,

      // Memory
      globalMemoryGB: 6,
      sharedMemoryPerSMKB: 100,
      sharedMemoryPerBlockKB: 48,
      l2CacheMB: 12,
      registerFilePerSMKB: 256,

      // Bandwidth
      memoryBandwidthGBs: 192,        // GDDR6 96-bit @ 16 Gbps = 192 GB/s
      memBandwidthGBs: 192,
      l2BandwidthGBs: 900,
      sharedMemBandwidthGBs: 2500,

      // Clock
      baseClockMHz: 1605,
      boostClockMHz: 2130,
      memoryClockMHz: 2000,

      // Interconnect
      nvlinkBandwidthGBs: 0,
      nvlinkConnections: 0,
      pcieGen: 4,
      pcieLanes: 8,
      pcieBandwidthGBs: 15.75,

      // Compute
      fp32CoresPerSM: 128,
      fp64CoresPerSM: 2,
      tensorCoresPerSM: 4,
      fp32TFLOPS: 10.9,
      fp16TFLOPS: 87.2,
      fp64TFLOPS: 0.17,

      sharedMemBanks: 32,
      sharedMemBankWidthBytes: 4,
      maxGridDimX: 2147483647,
      maxGridDimY: 65535,
      maxGridDimZ: 65535,
      maxBlockDimX: 1024,
      maxBlockDimY: 1024,
      maxBlockDimZ: 64,
      maxRegistersPerThread: 255,
      maxRegistersPerBlock: 65536,
      globalCacheLineSizeBytes: 128,
      sectorSizeBytes: 32,
      globalMemLatencyCycles: 280,
      sharedMemLatencyCycles: 22,
      l2CacheLatencyCycles: 180,
      arithmeticLatencyCycles: 4,
      syncthreadsLatencyCycles: 16
    },

    // =========================================================================
    // NVIDIA GeForce RTX 3090 — Ampere Consumer Flagship (GA102)
    // =========================================================================
    'RTX 3090': {
      name: 'NVIDIA GeForce RTX 3090',
      architecture: 'Ampere',
      computeCapability: '8.6',

      // Streaming Multiprocessors
      smCount: 82,
      maxThreadsPerSM: 1536,
      maxThreadsPerBlock: 1024,
      maxBlocksPerSM: 16,
      warpSize: 32,

      // Memory
      globalMemoryGB: 24,
      sharedMemoryPerSMKB: 100,       // max configurable shared memory per SM
      sharedMemoryPerBlockKB: 48,     // default shared memory per block
      l2CacheMB: 6,
      registerFilePerSMKB: 256,       // 65536 x 32-bit registers = 256 KB

      // Bandwidth
      memoryBandwidthGBs: 936,        // GDDR6X 384-bit @ 19.5 Gbps
      l2BandwidthGBs: 2500,           // approximate
      sharedMemBandwidthGBs: 14000,   // approximate aggregate across all SMs

      // Clock
      baseClockMHz: 1395,
      boostClockMHz: 1695,
      memoryClockMHz: 1219,           // GDDR6X actual clock (19.5 Gbps effective)

      // Interconnect (RTX 3090 supports NVLink bridge)
      nvlinkBandwidthGBs: 112.5,     // NVLink 3.0 bridge (single link, bidirectional)
      nvlinkConnections: 1,
      pcieGen: 4,
      pcieLanes: 16,
      pcieBandwidthGBs: 31.5,

      // Compute
      fp32CoresPerSM: 128,
      fp64CoresPerSM: 2,              // GA102 has 1:64 FP64:FP32 ratio
      tensorCoresPerSM: 4,            // 3rd gen Tensor Cores
      fp32TFLOPS: 35.6,
      fp16TFLOPS: 142.0,              // with sparsity
      fp64TFLOPS: 0.56,               // very limited FP64 on consumer Ampere

      // Shared memory bank configuration
      sharedMemBanks: 32,
      sharedMemBankWidthBytes: 4,

      // Execution limits
      maxGridDimX: 2147483647,
      maxGridDimY: 65535,
      maxGridDimZ: 65535,
      maxBlockDimX: 1024,
      maxBlockDimY: 1024,
      maxBlockDimZ: 64,
      maxRegistersPerThread: 255,
      maxRegistersPerBlock: 65536,

      // Cache line sizes
      globalCacheLineSizeBytes: 128,
      sectorSizeBytes: 32,

      // Latencies (approximate cycles)
      globalMemLatencyCycles: 290,
      sharedMemLatencyCycles: 23,
      l2CacheLatencyCycles: 200,
      arithmeticLatencyCycles: 4,
      syncthreadsLatencyCycles: 16
    },

    // =========================================================================
    // NVIDIA Tesla T4 16GB — Turing (TU104), PCIe, 70 W inference card
    // Values from NVIDIA's published T4 datasheet; latencies approximate.
    // =========================================================================
    'T4': {
      name: 'NVIDIA Tesla T4 16GB',
      architecture: 'Turing',
      computeCapability: '7.5',
      smCount: 40,
      maxThreadsPerSM: 1024,
      maxThreadsPerBlock: 1024,
      maxBlocksPerSM: 16,
      warpSize: 32,
      globalMemoryGB: 16,
      sharedMemoryPerSMKB: 64,
      sharedMemoryPerBlockKB: 48,
      l2CacheMB: 4,
      registerFilePerSMKB: 256,
      memoryBandwidthGBs: 320,        // GDDR6 peak
      l2BandwidthGBs: 1300,
      sharedMemBandwidthGBs: 5000,
      baseClockMHz: 585,
      boostClockMHz: 1590,
      memoryClockMHz: 5001,
      nvlinkBandwidthGBs: 0,
      nvlinkConnections: 0,
      pcieGen: 3,
      pcieLanes: 16,
      pcieBandwidthGBs: 15.75,
      fp32CoresPerSM: 64,
      fp64CoresPerSM: 2,
      tensorCoresPerSM: 8,
      fp32TFLOPS: 8.1,
      fp16TFLOPS: 65.0,
      fp64TFLOPS: 0.25,
      sharedMemBanks: 32,
      sharedMemBankWidthBytes: 4,
      maxGridDimX: 2147483647,
      maxGridDimY: 65535,
      maxGridDimZ: 65535,
      maxBlockDimX: 1024,
      maxBlockDimY: 1024,
      maxBlockDimZ: 64,
      maxRegistersPerThread: 255,
      maxRegistersPerBlock: 65536,
      globalCacheLineSizeBytes: 128,
      sectorSizeBytes: 32,
      globalMemLatencyCycles: 330,
      sharedMemLatencyCycles: 22,
      l2CacheLatencyCycles: 200,
      arithmeticLatencyCycles: 4,
      syncthreadsLatencyCycles: 16
    },

    // =========================================================================
    // NVIDIA V100 32GB (SXM2) — Volta Data Center GPU (GV100)
    // =========================================================================
    'V100': {
      name: 'NVIDIA V100 32GB SXM2',
      architecture: 'Volta',
      computeCapability: '7.0',

      // Streaming Multiprocessors
      smCount: 80,
      maxThreadsPerSM: 2048,
      maxThreadsPerBlock: 1024,
      maxBlocksPerSM: 32,
      warpSize: 32,

      // Memory
      globalMemoryGB: 32,
      sharedMemoryPerSMKB: 96,        // max configurable shared memory per SM
      sharedMemoryPerBlockKB: 48,     // default shared memory per block (up to 96 KB)
      l2CacheMB: 6,
      registerFilePerSMKB: 256,       // 65536 x 32-bit registers = 256 KB

      // Bandwidth
      memoryBandwidthGBs: 900,        // HBM2 peak bandwidth
      l2BandwidthGBs: 3000,           // approximate aggregate L2 bandwidth
      sharedMemBandwidthGBs: 13000,   // approximate aggregate across all SMs

      // Clock
      baseClockMHz: 1290,
      boostClockMHz: 1530,
      memoryClockMHz: 877,            // HBM2 actual clock (1754 MHz effective)

      // Interconnect
      nvlinkBandwidthGBs: 300,        // total bidirectional NVLink 2.0 bandwidth
      nvlinkConnections: 6,           // NVLink 2.0 links (SXM2)
      pcieGen: 3,
      pcieLanes: 16,
      pcieBandwidthGBs: 15.75,

      // Compute
      fp32CoresPerSM: 64,
      fp64CoresPerSM: 32,
      tensorCoresPerSM: 8,            // 1st gen Tensor Cores
      fp32TFLOPS: 15.7,               // SXM2 variant
      fp16TFLOPS: 125.0,              // Tensor Core mixed precision (SXM2)
      fp64TFLOPS: 7.8,

      // Shared memory bank configuration
      sharedMemBanks: 32,
      sharedMemBankWidthBytes: 4,

      // Execution limits
      maxGridDimX: 2147483647,
      maxGridDimY: 65535,
      maxGridDimZ: 65535,
      maxBlockDimX: 1024,
      maxBlockDimY: 1024,
      maxBlockDimZ: 64,
      maxRegistersPerThread: 255,
      maxRegistersPerBlock: 65536,

      // Cache line sizes
      globalCacheLineSizeBytes: 128,
      sectorSizeBytes: 32,

      // Latencies (approximate cycles — Volta has higher latency than Ampere)
      globalMemLatencyCycles: 350,
      sharedMemLatencyCycles: 28,
      l2CacheLatencyCycles: 220,
      arithmeticLatencyCycles: 4,
      syncthreadsLatencyCycles: 16
    }
  };

  // ===========================================================================
  // Helper functions
  // ===========================================================================

  /**
   * Retrieve a GPU profile by name. Supports partial matching and
   * case-insensitive lookup. Returns the A100 profile as the default
   * if no match is found.
   *
   * @param {string} name - GPU model name (e.g. 'A100', 'RTX 4090', 'H100')
   * @returns {Object} The matching GPU profile object
   */
  function getProfile(name) {
    if (!name || typeof name !== 'string') {
      return profiles['A100'];
    }

    // Direct key match
    if (profiles[name]) {
      return profiles[name];
    }

    // Case-insensitive & whitespace/underscore-agnostic match against keys
    var normName = name.toUpperCase().replace(/[\s_-]+/g, '');
    var keys = Object.keys(profiles);
    for (var i = 0; i < keys.length; i++) {
      if (keys[i].toUpperCase().replace(/[\s_-]+/g, '') === normName) {
        return profiles[keys[i]];
      }
    }

    // Partial match against the full profile name
    for (var j = 0; j < keys.length; j++) {
      if (profiles[keys[j]].name.toUpperCase().indexOf(upperName) !== -1) {
        return profiles[keys[j]];
      }
    }

    // Partial match against keys
    for (var k = 0; k < keys.length; k++) {
      if (upperName.indexOf(keys[k].toUpperCase()) !== -1 ||
          keys[k].toUpperCase().indexOf(upperName) !== -1) {
        return profiles[keys[k]];
      }
    }

    // Default to A100
    return profiles['A100'];
  }

  /**
   * List all available GPU profile names.
   *
   * @returns {string[]} Array of profile key names
   */
  function listProfiles() {
    return Object.keys(profiles);
  }

  // ===========================================================================
  // Export to window.GPU_PROFILES
  // ===========================================================================

  // Copy all profile entries onto the export object
  var exported = {};
  var allKeys = Object.keys(profiles);
  for (var i = 0; i < allKeys.length; i++) {
    var p = profiles[allKeys[i]];
    if (p && typeof p === 'object') {
      if (p.memoryBandwidthGBs && !p.memBandwidthGBs) {
        p.memBandwidthGBs = p.memoryBandwidthGBs;
      }
      if (p.memBandwidthGBs && !p.memoryBandwidthGBs) {
        p.memoryBandwidthGBs = p.memBandwidthGBs;
      }
    }
    exported[allKeys[i]] = p;
  }

  // Attach helper functions
  exported.getProfile = getProfile;
  exported.listProfiles = listProfiles;

  // globalThis works on the main thread and inside Web Workers (no `window`)
  if (typeof globalThis !== 'undefined') {
    globalThis.GPU_PROFILES = exported;
  }
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = exported;
  }
  if (typeof globalThis !== 'undefined') {
    globalThis.GPU_PROFILES = exported;
  }
})();
