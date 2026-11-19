/**
 * demo/fp16-bf16.js
 * ─────────────────
 * IEEE-754 binary16 (Half Precision) and Google/NVIDIA bfloat16
 * conversion and arithmetic emulation with Round-to-Nearest-Even (Ties to Even).
 */

(function () {
  'use strict';

  const f32Buf = new Float32Array(1);
  const u32Buf = new Uint32Array(f32Buf.buffer);

  // ═══════════════════════════════════════════════════════════════════════════
  // IEEE-754 binary16 (Half) Conversion & Arithmetic
  // ═══════════════════════════════════════════════════════════════════════════

  /**
   * Converts Float32 to IEEE-754 binary16 uint16 with round-to-nearest-even.
   * Handles infinities, NaNs, normal, subnormal, and ties-to-even.
   * @param {number} val
   * @returns {number} 16-bit unsigned integer
   */
  function float2half(val) {
    f32Buf[0] = val;
    const x = u32Buf[0];
    const sign = (x >>> 31) & 1;
    const exp = (x >>> 23) & 0xff;
    const frac = x & 0x7fffff;

    // Special cases: NaN or Infinity
    if (exp === 0xff) {
      if (frac === 0) {
        // Infinity
        return (sign << 15) | 0x7c00;
      }
      // NaN - preserve quiet NaN payload bit
      return (sign << 15) | 0x7c00 | 0x0200 | (frac >>> 13);
    }

    // Zero
    if (exp === 0 && frac === 0) {
      return sign << 15;
    }

    let newExp = exp - 127 + 15;

    // Overflow to Infinity
    if (newExp >= 31) {
      return (sign << 15) | 0x7c00;
    }

    // Subnormal half or underflow to zero
    if (newExp <= 0) {
      if (newExp < -10) {
        return sign << 15; // Complete underflow to 0
      }
      const fullFrac = frac | 0x800000;
      const shift = 14 - newExp;
      const roundBit = (fullFrac >>> (shift - 1)) & 1;
      const stickyBits = fullFrac & ((1 << (shift - 1)) - 1);
      const lsb = (fullFrac >>> shift) & 1;
      let hFrac = fullFrac >>> shift;

      // Round to nearest even
      if (roundBit && (stickyBits || lsb)) {
        hFrac++;
      }
      return (sign << 15) | hFrac;
    }

    // Normal half
    const roundBit = (frac >>> 12) & 1;
    const stickyBits = frac & 0xfff;
    const lsb = (frac >>> 13) & 1;
    let hFrac = frac >>> 13;

    if (roundBit && (stickyBits || lsb)) {
      hFrac++;
      if (hFrac === 1024) {
        newExp++;
        hFrac = 0;
        if (newExp >= 31) {
          return (sign << 15) | 0x7c00;
        }
      }
    }

    return (sign << 15) | (newExp << 10) | hFrac;
  }

  /**
   * Converts IEEE-754 binary16 uint16 to Float32 number.
   * @param {number} h 16-bit unsigned integer
   * @returns {number}
   */
  function half2float(h) {
    const sign = (h >>> 15) & 1;
    const exp = (h >>> 10) & 0x1f;
    const frac = h & 0x3ff;

    if (exp === 0x1f) {
      u32Buf[0] = (sign << 31) | (0xff << 23) | (frac ? 0x400000 : 0);
      return f32Buf[0];
    }

    if (exp === 0) {
      if (frac === 0) {
        u32Buf[0] = sign << 31;
        return f32Buf[0];
      }
      // Subnormal
      let f = frac;
      let e = -14;
      while ((f & 0x400) === 0) {
        f <<= 1;
        e--;
      }
      f &= 0x3ff;
      u32Buf[0] = (sign << 31) | ((e + 127) << 23) | (f << 13);
      return f32Buf[0];
    }

    u32Buf[0] = (sign << 31) | ((exp - 15 + 127) << 23) | (frac << 13);
    return f32Buf[0];
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // bfloat16 Conversion & Arithmetic
  // ═══════════════════════════════════════════════════════════════════════════

  /**
   * Converts Float32 to bfloat16 uint16 with round-to-nearest-even.
   * @param {number} val
   * @returns {number} 16-bit unsigned integer
   */
  function float2bfloat16(val) {
    f32Buf[0] = val;
    const x = u32Buf[0];
    const exp = (x >>> 23) & 0xff;
    const frac = x & 0x7fffff;

    // Special cases: NaN or Infinity
    if (exp === 0xff) {
      return (x >>> 16) | (frac ? 0x40 : 0);
    }

    // Round to nearest even
    const lsb = (x >>> 16) & 1;
    const roundBit = (x >>> 15) & 1;
    const sticky = x & 0x7fff;
    let res = x >>> 16;
    if (roundBit && (sticky || lsb)) {
      res++;
    }
    return res & 0xffff;
  }

  /**
   * Converts bfloat16 uint16 to Float32 number.
   * @param {number} bf 16-bit unsigned integer
   * @returns {number}
   */
  function bfloat162float(bf) {
    u32Buf[0] = (bf & 0xffff) << 16;
    return f32Buf[0];
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // Arithmetic Intrinsics
  // ═══════════════════════════════════════════════════════════════════════════

  function hadd(a, b) {
    return float2half(half2float(a) + half2float(b));
  }
  function hsub(a, b) {
    return float2half(half2float(a) - half2float(b));
  }
  function hmul(a, b) {
    return float2half(half2float(a) * half2float(b));
  }
  function hdiv(a, b) {
    return float2half(half2float(a) / half2float(b));
  }
  function hneg(a) {
    return a ^ 0x8000;
  }

  function hadd_bf16(a, b) {
    return float2bfloat16(bfloat162float(a) + bfloat162float(b));
  }
  function hsub_bf16(a, b) {
    return float2bfloat16(bfloat162float(a) - bfloat162float(b));
  }
  function hmul_bf16(a, b) {
    return float2bfloat16(bfloat162float(a) * bfloat162float(b));
  }
  function hdiv_bf16(a, b) {
    return float2bfloat16(bfloat162float(a) / bfloat162float(b));
  }
  function hneg_bf16(a) {
    return a ^ 0x8000;
  }

  const exported = {
    float2half,
    half2float,
    float2bfloat16,
    bfloat162float,
    __float2half: float2half,
    __half2float: half2float,
    __float2bfloat16: float2bfloat16,
    __bfloat162float: bfloat162float,
    __hadd: hadd,
    __hsub: hsub,
    __hmul: hmul,
    __hdiv: hdiv,
    __hneg: hneg,
    __hadd_bf16: hadd_bf16,
    __hsub_bf16: hsub_bf16,
    __hmul_bf16: hmul_bf16,
    __hdiv_bf16: hdiv_bf16,
    __hneg_bf16: hneg_bf16
  };

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = exported;
  }
  // globalThis works on the main thread and inside Web Workers (no `window`)
  if (typeof globalThis !== 'undefined') {
    globalThis.GpuboxFP16 = exported;
  }
  if (typeof globalThis !== 'undefined') {
    globalThis.GpuboxFP16 = exported;
  }
})();
