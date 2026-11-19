/**
 * demo/topology-model.js
 * ──────────────────────
 * Cluster Interconnect Topology & Analytical Timing Model (1 to 16 GPUs).
 *
 * Models:
 *   - Topology presets: NVSwitch Mesh, PCIe Tree, Multi-Node (2x8 SXM + InfiniBand), Custom
 *   - 16x16 Pairwise Traffic Matrix (bytes transferred from rank i to rank j)
 *   - Alpha-Beta Analytical Timing Model: Time = alpha (latency) + bytes / beta (bandwidth)
 *   - Per-link utilization tracking
 *
 * NOTE: Estimated timings are calculated analytically from architecture models
 * and are labeled as simulated estimates, not physical measurements.
 */

(function () {
  'use strict';

  class ClusterTopology {
    /**
     * @param {Object} options
     * @param {string} [options.preset='nvswitch_mesh'] 'nvswitch_mesh' | 'pcie_tree' | 'multi_node' | 'custom'
     * @param {number} [options.nranks=16] 1 to 16 GPUs
     * @param {Object} [options.profile] GPU profile from gpu-profiles.js
     * @param {number[][]} [options.customMatrix] Custom 16x16 link bandwidth matrix in GB/s
     */
    constructor(options = {}) {
      this.nranks = Math.max(1, Math.min(16, options.nranks || 16));
      this.preset = options.preset || 'nvswitch_mesh';
      this.profile = options.profile || { name: 'A100', nvlinkBandwidthGBs: 600, pcieBandwidthGBs: 31.5 };

      // Initialize 16x16 link bandwidth matrix (GB/s)
      this.linkBandwidthGBs = Array.from({ length: 16 }, () => new Float64Array(16));

      // Initialize 16x16 traffic matrix (bytes transferred)
      this.trafficMatrix = Array.from({ length: 16 }, () => new Float64Array(16));

      // Latency alpha in microseconds (modeled estimates)
      this.alphaUs = 1.2; // default NVLink collective launch latency
      this.buildTopology(options.customMatrix);
    }

    buildTopology(customMatrix) {
      const nvlinkBW = this.profile.nvlinkBandwidthGBs || 600;
      const pcieBW = this.profile.pcieBandwidthGBs || 31.5;

      if (this.preset === 'custom' && customMatrix) {
        for (let i = 0; i < 16; i++) {
          for (let j = 0; j < 16; j++) {
            this.linkBandwidthGBs[i][j] = (customMatrix[i] && customMatrix[i][j]) || 0;
          }
        }
        return;
      }

      if (this.preset === 'nvswitch_mesh') {
        this.alphaUs = 1.0;
        for (let i = 0; i < 16; i++) {
          for (let j = 0; j < 16; j++) {
            if (i !== j) {
              this.linkBandwidthGBs[i][j] = nvlinkBW;
            }
          }
        }
      } else if (this.preset === 'pcie_tree') {
        this.alphaUs = 4.5;
        for (let i = 0; i < 16; i++) {
          for (let j = 0; j < 16; j++) {
            if (i !== j) {
              this.linkBandwidthGBs[i][j] = pcieBW;
            }
          }
        }
      } else if (this.preset === 'multi_node') {
        // 2 nodes x 8 GPUs: intra-node (0-7 and 8-15) via NVLink; inter-node via InfiniBand 400G (50 GB/s)
        this.alphaUs = 2.5;
        const ibBW = 50.0;
        for (let i = 0; i < 16; i++) {
          for (let j = 0; j < 16; j++) {
            if (i !== j) {
              const nodeI = Math.floor(i / 8);
              const nodeJ = Math.floor(j / 8);
              this.linkBandwidthGBs[i][j] = (nodeI === nodeJ) ? nvlinkBW : ibBW;
            }
          }
        }
      }
    }

    recordTransfer(srcRank, dstRank, bytes) {
      if (srcRank >= 0 && srcRank < 16 && dstRank >= 0 && dstRank < 16) {
        this.trafficMatrix[srcRank][dstRank] += bytes;
      }
    }

    /**
     * Compute analytical execution time using Alpha-Beta model.
     * Time = alpha (base latency) + bytes / effectiveBandwidth
     * @param {number} bytes Total transferred bytes
     * @param {string} op Collective operation name ('allreduce', 'broadcast', etc.)
     * @returns {Object} Estimated timing report
     */
    estimateCollectiveTime(bytes, op = 'allreduce') {
      const n = this.nranks;
      if (n <= 1 || bytes <= 0) {
        return { modeledTimeUs: 0.1, alphaUs: this.alphaUs, effectiveBandwidthGBs: 0 };
      }

      let bw = this.linkBandwidthGBs[0][1] || 100;
      // Ring AllReduce algorithm: 2*(n-1)/n * bytes per rank across 2*(n-1) steps
      const steps = (op === 'allreduce' || op === 'reducescatter' || op === 'allgather') ? 2 * (n - 1) : Math.ceil(Math.log2(n));
      const totalAlphaUs = this.alphaUs * steps;
      const transferTimeUs = (bytes / (bw * 1e9)) * 1e6;
      const totalTimeUs = totalAlphaUs + transferTimeUs;

      return {
        modeledTimeUs: parseFloat(totalTimeUs.toFixed(3)),
        alphaUs: parseFloat(totalAlphaUs.toFixed(3)),
        effectiveBandwidthGBs: bw,
        modelLabel: 'ANALYTICAL_ALPHA_BETA_ESTIMATE'
      };
    }

    getTrafficMatrix() {
      const res = [];
      for (let i = 0; i < this.nranks; i++) {
        const row = [];
        for (let j = 0; j < this.nranks; j++) {
          row.push(this.trafficMatrix[i][j]);
        }
        res.push(row);
      }
      return res;
    }

    reset() {
      for (let i = 0; i < 16; i++) {
        this.trafficMatrix[i].fill(0);
      }
    }
  }

  const exported = {
    ClusterTopology
  };

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = exported;
  }
  // globalThis works on the main thread and inside Web Workers (no `window`)
  if (typeof globalThis !== 'undefined') {
    globalThis.GpuboxTopology = exported;
  }
  if (typeof globalThis !== 'undefined') {
    globalThis.GpuboxTopology = exported;
  }
})();
