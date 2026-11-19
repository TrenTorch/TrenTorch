/**
 * validation-harness.js
 *
 * Expected-vs-actual validation harness for Gpubox.
 * Supports absolute, relative, and ULP tolerance comparisons.
 *
 * Copyright (c) 2026 Aadityansha Verma. All rights reserved.
 */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.GpuboxValidation = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  const f32Buf = new Float32Array(1);
  const u32Buf = new Uint32Array(f32Buf.buffer);

  function floatToUint32Bits(f) {
    f32Buf[0] = f;
    return u32Buf[0];
  }

  /**
   * Compute ULP distance between two IEEE-754 binary32 floats.
   */
  function float32UlpDiff(a, b) {
    if (a === b) return 0;
    if (Number.isNaN(a) || Number.isNaN(b)) return Infinity;
    if (!Number.isFinite(a) || !Number.isFinite(b)) return Infinity;

    const uA = floatToUint32Bits(a);
    const uB = floatToUint32Bits(b);

    // If both are zero (+0 or -0)
    if ((uA & 0x7FFFFFFF) === 0 && (uB & 0x7FFFFFFF) === 0) return 0;

    // Convert sign-magnitude to two's complement integer
    let intA = (uA & 0x80000000) ? (0x80000000 - (uA & 0x7FFFFFFF)) : uA;
    let intB = (uB & 0x80000000) ? (0x80000000 - (uB & 0x7FFFFFFF)) : uB;

    return Math.abs(intA - intB);
  }

  /**
   * Validate actual array against expected array.
   *
   * @param {ArrayLike<number>} actual
   * @param {ArrayLike<number>} expected
   * @param {object} [options]
   * @param {'abs'|'relative'|'ulp'} [options.mode='abs']
   * @param {number} [options.tolerance]
   * @param {number} [options.absTol]
   * @param {number} [options.relTol]
   * @param {number} [options.maxUlps]
   * @returns {{
   *   verdict: 'PASS' | 'FAIL',
   *   totalElements: number,
   *   mismatchCount: number,
   *   firstMismatch: { index: number, expected: number, actual: number, absError: number, relError: number, ulpDiff?: number } | null
   * }}
   */
  function validateOutput(actual, expected, options = {}) {
    const mode = options.mode || 'abs';
    const absTol = options.absTol !== undefined ? options.absTol : (options.tolerance !== undefined ? options.tolerance : 1e-5);
    const relTol = options.relTol !== undefined ? options.relTol : (options.tolerance !== undefined ? options.tolerance : 1e-4);
    const maxUlps = options.maxUlps !== undefined ? options.maxUlps : (options.tolerance !== undefined ? options.tolerance : 4);

    const actLen = actual.length !== undefined ? actual.length : 0;
    const expLen = expected.length !== undefined ? expected.length : 0;

    if (actLen !== expLen) {
      return {
        verdict: 'FAIL',
        totalElements: Math.max(actLen, expLen),
        mismatchCount: Math.abs(actLen - expLen),
        firstMismatch: {
          index: Math.min(actLen, expLen),
          expected: expected[Math.min(actLen, expLen)],
          actual: actual[Math.min(actLen, expLen)],
          absError: NaN,
          relError: NaN,
          reason: `Length mismatch: actual has ${actLen} elements, expected ${expLen}`
        }
      };
    }

    let mismatchCount = 0;
    let firstMismatch = null;

    for (let i = 0; i < expLen; i++) {
      const act = actual[i];
      const exp = expected[i];

      let match = false;
      const absErr = Math.abs(act - exp);
      const relErr = Math.abs(exp) > 1e-12 ? (absErr / Math.abs(exp)) : absErr;
      let ulpErr = 0;

      if (mode === 'abs') {
        match = absErr <= (absTol + 1e-12);
      } else if (mode === 'relative') {
        if (Math.abs(exp) <= 1e-9) {
          match = absErr <= ((options.absTol !== undefined ? options.absTol : 1e-5) + 1e-12);
        } else {
          match = relErr <= (relTol + 1e-12);
        }
      } else if (mode === 'ulp') {
        ulpErr = float32UlpDiff(act, exp);
        match = ulpErr <= maxUlps;
      } else {
        match = absErr <= absTol;
      }

      if (!match) {
        mismatchCount++;
        if (!firstMismatch) {
          firstMismatch = {
            index: i,
            expected: exp,
            actual: act,
            absError: absErr,
            relError: relErr,
            ...(mode === 'ulp' ? { ulpDiff: ulpErr } : {})
          };
        }
      }
    }

    return {
      verdict: mismatchCount === 0 ? 'PASS' : 'FAIL',
      totalElements: expLen,
      mismatchCount,
      firstMismatch
    };
  }

  return {
    validateOutput,
    float32UlpDiff
  };
}));
