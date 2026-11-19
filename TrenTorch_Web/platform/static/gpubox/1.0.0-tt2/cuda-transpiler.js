/**
 * CUDA C++ to JavaScript Transpiler
 * 
 * Converts raw CUDA C++ source code into executable JavaScript that runs
 * on the CudaRuntime simulator (window.CudaRuntime).
 * 
 * Usage:
 *   const result = CudaTranspiler.transpile(cudaSourceString);
 *   // result: { success, code, errors, kernelNames, warnings }
 *   if (result.success) {
 *     const fn = new Function('__rt', result.code);
 *     fn(runtimeInstance);
 *   }
 * 
 * The transpiler works in multiple passes:
 *   Pass 1: Preprocess — strip includes, handle #define, sizeof
 *   Pass 2: Extract and transform __global__ kernel functions
 *   Pass 3: Transform host code — main(), CUDA API calls, memory ops
 *   Pass 4: Transform expressions — math functions, type casts, pointer ops
 *   Pass 5: Fix syntax — C++ to JS syntax differences
 */
(function() {
  'use strict';

  // ---------------------------------------------------------------------------
  // Helpers
  // ---------------------------------------------------------------------------

  /**
   * Find the matching closing delimiter starting from a given offset.
   * Handles nested pairs: (), {}, [], <>.
   * @param {string} src   Source text
   * @param {number} start Index of the opening delimiter
   * @param {string} open  Opening char, e.g. '('
   * @param {string} close Closing char, e.g. ')'
   * @returns {number} Index of the matching closing delimiter, or -1
   */
  function findMatchingDelimiter(src, start, open, close) {
    let depth = 0;
    let inString = false;
    let stringChar = '';
    for (let i = start; i < src.length; i++) {
      const ch = src[i];
      if (inString) {
        if (ch === '\\') { i++; continue; }
        if (ch === stringChar) inString = false;
        continue;
      }
      if (ch === '"' || ch === "'") {
        inString = true;
        stringChar = ch;
        continue;
      }
      if (ch === open) depth++;
      else if (ch === close) {
        depth--;
        if (depth === 0) return i;
      }
    }
    return -1;
  }

  /**
   * Protect string literals and comments from being transformed.
   * Replaces them with placeholders and returns a restore function.
   */
  function protectStringsAndComments(src) {
    const saved = [];
    let idx = 0;

    // Replace block comments
    src = src.replace(/\/\*[\s\S]*?\*\//g, function(m) {
      const key = '\x00BLOCK' + (idx++) + '\x00';
      saved.push({ key: key, val: m });
      return key;
    });

    // Replace single-line comments
    src = src.replace(/\/\/[^\n]*/g, function(m) {
      const key = '\x00LINE' + (idx++) + '\x00';
      saved.push({ key: key, val: m });
      return key;
    });

    // Replace string literals (double-quoted)
    src = src.replace(/"(?:[^"\\]|\\.)*"/g, function(m) {
      const key = '\x00STR' + (idx++) + '\x00';
      saved.push({ key: key, val: m });
      return key;
    });

    // Replace char literals
    src = src.replace(/'(?:[^'\\]|\\.)*'/g, function(m) {
      const key = '\x00CHR' + (idx++) + '\x00';
      saved.push({ key: key, val: m });
      return key;
    });

    function restore(text) {
      // Restore in reverse order to handle nested placeholders
      for (let i = saved.length - 1; i >= 0; i--) {
        text = text.split(saved[i].key).join(saved[i].val);
      }
      return text;
    }

    return { text: src, restore: restore };
  }

  /**
   * Extract argument list from a parenthesized expression starting at pos.
   * Returns { args: string[], end: number } where end is the index past ')'.
   */
  function extractArgs(src, parenOpen) {
    const parenClose = findMatchingDelimiter(src, parenOpen, '(', ')');
    if (parenClose === -1) return { args: [], end: parenOpen + 1 };
    const inner = src.substring(parenOpen + 1, parenClose).trim();
    if (inner.length === 0) return { args: [], end: parenClose + 1 };

    // Split on commas that are not inside nested parens/brackets
    const args = [];
    let depth = 0;
    let current = '';
    for (let i = 0; i < inner.length; i++) {
      const ch = inner[i];
      if (ch === '(' || ch === '[' || ch === '{') depth++;
      else if (ch === ')' || ch === ']' || ch === '}') depth--;
      else if (ch === ',' && depth === 0) {
        args.push(current.trim());
        current = '';
        continue;
      }
      current += ch;
    }
    if (current.trim().length > 0) args.push(current.trim());
    return { args: args, end: parenClose + 1 };
  }

  // ---------------------------------------------------------------------------
  // sizeof map
  // ---------------------------------------------------------------------------
  const SIZEOF_MAP = {
    'char': 1, 'unsigned char': 1, 'uint8_t': 1, 'int8_t': 1,
    'short': 2, 'unsigned short': 2, 'uint16_t': 2, 'int16_t': 2, 'half': 2,
    'int': 4, 'unsigned int': 4, 'uint32_t': 4, 'int32_t': 4,
    'float': 4,
    'long': 4, 'unsigned long': 4,
    'long long': 8, 'unsigned long long': 8,
    'double': 8, 'uint64_t': 8, 'int64_t': 8, 'size_t': 8,
    'float2': 8, 'int2': 8,
    'float4': 16, 'int4': 16, 'double2': 16,
  };

  // ---------------------------------------------------------------------------
  // Math function map
  // ---------------------------------------------------------------------------
  const MATH_FUNCS = {
    'expf':        { js: 'Math.exp',   nargs: 1 },
    '__expf':      { js: 'Math.exp',   nargs: 1 },
    'exp':         { js: 'Math.exp',   nargs: 1 },
    'logf':        { js: 'Math.log',   nargs: 1 },
    'log':         { js: 'Math.log',   nargs: 1 },
    'log2f':       { js: 'Math.log2',  nargs: 1 },
    'log10f':      { js: 'Math.log10', nargs: 1 },
    'sqrtf':       { js: 'Math.sqrt',  nargs: 1 },
    'sqrt':        { js: 'Math.sqrt',  nargs: 1 },
    'fabsf':       { js: 'Math.abs',   nargs: 1 },
    'fabs':        { js: 'Math.abs',   nargs: 1 },
    'abs':         { js: 'Math.abs',   nargs: 1 },
    'fmaxf':       { js: 'Math.max',   nargs: 2 },
    'fmax':        { js: 'Math.max',   nargs: 2 },
    'max':         { js: 'Math.max',   nargs: 2 },
    'fminf':       { js: 'Math.min',   nargs: 2 },
    'fmin':        { js: 'Math.min',   nargs: 2 },
    'min':         { js: 'Math.min',   nargs: 2 },
    'powf':        { js: 'Math.pow',   nargs: 2 },
    'pow':         { js: 'Math.pow',   nargs: 2 },
    'sinf':        { js: 'Math.sin',   nargs: 1 },
    'sin':         { js: 'Math.sin',   nargs: 1 },
    'cosf':        { js: 'Math.cos',   nargs: 1 },
    'cos':         { js: 'Math.cos',   nargs: 1 },
    'tanf':        { js: 'Math.tan',   nargs: 1 },
    'tan':         { js: 'Math.tan',   nargs: 1 },
    'tanhf':       { js: 'Math.tanh',  nargs: 1 },
    'tanh':        { js: 'Math.tanh',  nargs: 1 },
    'sinhf':       { js: 'Math.sinh',  nargs: 1 },
    'coshf':       { js: 'Math.cosh',  nargs: 1 },
    'atanf':       { js: 'Math.atan',  nargs: 1 },
    'atan2f':      { js: 'Math.atan2', nargs: 2 },
    'asinf':       { js: 'Math.asin',  nargs: 1 },
    'acosf':       { js: 'Math.acos',  nargs: 1 },
    'ceilf':       { js: 'Math.ceil',  nargs: 1 },
    'ceil':        { js: 'Math.ceil',  nargs: 1 },
    'floorf':      { js: 'Math.floor', nargs: 1 },
    'floor':       { js: 'Math.floor', nargs: 1 },
    'roundf':      { js: 'Math.round', nargs: 1 },
    'round':       { js: 'Math.round', nargs: 1 },
    'truncf':      { js: 'Math.trunc', nargs: 1 },
    'trunc':       { js: 'Math.trunc', nargs: 1 },
    'erff':        { js: null, nargs: 1, template: '__erf($1)' },
    'erf':         { js: null, nargs: 1, template: '__erf($1)' },
    'rsqrtf':      { js: null, nargs: 1, template: '(1.0/Math.sqrt($1))' },
    'rsqrt':       { js: null, nargs: 1, template: '(1.0/Math.sqrt($1))' },
    '__rsqrtf':    { js: null, nargs: 1, template: '(1.0/Math.sqrt($1))' },
    'fmaf':        { js: null, nargs: 3, template: '($1*$2+$3)' },
    'fma':         { js: null, nargs: 3, template: '($1*$2+$3)' },
    '__fmaf_rn':   { js: null, nargs: 3, template: '($1*$2+$3)' },
    '__fmul_rn':   { js: null, nargs: 2, template: '($1*$2)' },
    '__fadd_rn':   { js: null, nargs: 2, template: '($1+$2)' },
    '__fdividef':  { js: null, nargs: 2, template: '($1/$2)' },
    '__saturatef': { js: null, nargs: 1, template: 'Math.max(0.0, Math.min(1.0, $1))' },
    'isinf':       { js: null, nargs: 1, template: '(!Number.isFinite($1) && !Number.isNaN($1))' },
    'isinff':      { js: null, nargs: 1, template: '(!Number.isFinite($1) && !Number.isNaN($1))' },
    '__isinf':     { js: null, nargs: 1, template: '(!Number.isFinite($1) && !Number.isNaN($1))' },
    '__isinff':    { js: null, nargs: 1, template: '(!Number.isFinite($1) && !Number.isNaN($1))' },
    'isnan':       { js: 'Number.isNaN', nargs: 1 },
    'isnanf':      { js: 'Number.isNaN', nargs: 1 },
    '__isnan':     { js: 'Number.isNaN', nargs: 1 },
    '__isnanf':    { js: 'Number.isNaN', nargs: 1 },
    'isfinite':    { js: 'Number.isFinite', nargs: 1 },
    'isfinitef':   { js: 'Number.isFinite', nargs: 1 },
    '__finite':    { js: 'Number.isFinite', nargs: 1 },
    '__finitef':   { js: 'Number.isFinite', nargs: 1 },
    'signbit':     { js: null, nargs: 1, template: '(Math.sign($1) < 0 || Object.is($1, -0))' },
    'signbitf':    { js: null, nargs: 1, template: '(Math.sign($1) < 0 || Object.is($1, -0))' },
    'copysign':    { js: null, nargs: 2, template: '(Math.sign($2) === 0 ? Math.abs($1) : Math.abs($1) * Math.sign($2))' },
    'copysignf':   { js: null, nargs: 2, template: '(Math.sign($2) === 0 ? Math.abs($1) : Math.abs($1) * Math.sign($2))' },
    'hypot':       { js: 'Math.hypot', nargs: 2 },
    'hypotf':      { js: 'Math.hypot', nargs: 2 },
    'cbrt':        { js: 'Math.cbrt',  nargs: 1 },
    'cbrtf':       { js: 'Math.cbrt',  nargs: 1 },
    'expm1':       { js: 'Math.expm1', nargs: 1 },
    'expm1f':      { js: 'Math.expm1', nargs: 1 },
    'log1p':       { js: 'Math.log1p', nargs: 1 },
    'log1pf':      { js: 'Math.log1p', nargs: 1 },
    'exp2':        { js: null, nargs: 1, template: 'Math.pow(2, $1)' },
    'exp2f':       { js: null, nargs: 1, template: 'Math.pow(2, $1)' },
    'exp10':       { js: null, nargs: 1, template: 'Math.pow(10, $1)' },
    'exp10f':      { js: null, nargs: 1, template: 'Math.pow(10, $1)' },
    '__exp10f':    { js: null, nargs: 1, template: 'Math.pow(10, $1)' },
    'fmod':        { js: null, nargs: 2, template: '($1 % $2)' },
    'fmodf':       { js: null, nargs: 2, template: '($1 % $2)' },
  };

  // ---------------------------------------------------------------------------
  // C type to JS typed-array map (for host allocations)
  // ---------------------------------------------------------------------------
  const TYPE_TO_ARRAY = {
    'float':  'Float32Array',
    'double': 'Float64Array',
    'int':    'Int32Array',
    'unsigned int': 'Uint32Array',
    'uint32_t': 'Uint32Array',
    'int32_t':  'Int32Array',
    'short':  'Int16Array',
    'unsigned short': 'Uint16Array',
    'char':   'Int8Array',
    'unsigned char': 'Uint8Array',
    'uint8_t': 'Uint8Array',
    'int8_t':  'Int8Array',
    'long long': 'BigInt64Array',
    'uint64_t': 'BigUint64Array',
    'int64_t':  'BigInt64Array',
  };

  // ---------------------------------------------------------------------------
  // Constant replacements
  // ---------------------------------------------------------------------------
  const CONSTANT_MAP = {
    'FLT_MAX':   '3.402823466e+38',
    'FLT_MIN':   '1.175494351e-38',
    'FLT_EPSILON': '1.192092896e-07',
    'DBL_MAX':   '1.7976931348623157e+308',
    'INT_MAX':   '2147483647',
    'INT_MIN':   '-2147483648',
    'UINT_MAX':  '4294967295',
    'INFINITY':  'Infinity',
    'NAN':       'NaN',
    'M_PI':      'Math.PI',
    'M_PI_F':    'Math.PI',
    'NULL':      'null',
    'nullptr':   'null',
    'true':      'true',
    'false':     'false',
    'WARP_SIZE': '32',
    'warpSize':  '32',
    'cudaSuccess': '0',
  };

  // ---------------------------------------------------------------------------
  // Pass 1: Preprocessor
  // ---------------------------------------------------------------------------

  /**
   * Handle preprocessor directives.
   * - Strips #include
   * - Converts simple #define to const/function
   * - Strips #ifdef/#ifndef/#else/#endif blocks (keeps code, strips directives)
   * - Replaces sizeof(type)
   */
  function preprocessorPass(src, warnings) {
    // Flatten backslash-continued lines: #define CHECK(x) \ ...
    src = src.replace(/\\\r?\n/g, ' ');

    const lines = src.split('\n');
    const output = [];
    const globalMacros = [];

    for (let i = 0; i < lines.length; i++) {
      let line = lines[i];
      const trimmed = line.trim();

      // Strip #include
      if (/^#\s*include\b/.test(trimmed)) {
        output.push(''); // keep line numbers stable
        continue;
      }

      // #pragma — strip
      if (/^#\s*pragma\b/.test(trimmed)) {
        output.push('');
        continue;
      }

      // #ifdef, #ifndef, #if, #else, #elif, #endif — just strip the directive, keep the code
      if (/^#\s*(ifdef|ifndef|if|else|elif|endif)\b/.test(trimmed)) {
        output.push('');
        continue;
      }

      // #define NAME(args) expr  → function macro
      const macroFnMatch = trimmed.match(/^#\s*define\s+(\w+)\(([^)]*)\)\s+(.+)$/);
      if (macroFnMatch) {
        const name = macroFnMatch[1];
        const params = macroFnMatch[2];
        let body = macroFnMatch[3].trim();
        // If it's a multi-statement, do-while, or block macro, emit a passthrough function
        if (body.includes('{') || body.includes(';') || body.startsWith('do')) {
          globalMacros.push('function ' + name + '(...args) { return args[0]; }');
        } else {
          globalMacros.push('function ' + name + '(' + params + ') { return ' + body + '; }');
        }
        output.push('');
        continue;
      }

      // #define NAME value → const
      const macroValMatch = trimmed.match(/^#\s*define\s+(\w+)\s+(.+)$/);
      if (macroValMatch) {
        const name = macroValMatch[1];
        let value = macroValMatch[2].trim();
        // Strip trailing comments, protected comment tokens, and clean float literals
        value = value.replace(/\x00[A-Z]+\d+\x00/g, '').replace(/\/\/.*$/, '').replace(/\/\*.*?\*\//g, '').replace(/(\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)f\b/g, '$1').trim();
        globalMacros.push('const ' + name + ' = ' + value + ';');
        output.push('');
        continue;
      }

      // #define NAME (no value) — just strip
      if (/^#\s*define\s+\w+\s*$/.test(trimmed)) {
        output.push('');
        continue;
      }

      // #undef — strip
      if (/^#\s*undef\b/.test(trimmed)) {
        output.push('');
        continue;
      }

      output.push(line);
    }

    src = output.join('\n');

    // Replace sizeof(type) or sizeof(var) with numeric/byte values
    src = src.replace(/sizeof\s*\(\s*([^)]+)\s*\)/g, function(match, typeName) {
      typeName = typeName.trim().replace(/\s+/g, ' ');
      // Remove pointer stars for sizeof
      const baseType = typeName.replace(/\s*\*\s*/g, '');
      if (SIZEOF_MAP[baseType] !== undefined) {
        return String(SIZEOF_MAP[baseType]);
      }
      // If it's a variable or array name, use its byteLength if available
      return '(typeof ' + typeName + " !== 'undefined' && " + typeName + '.byteLength !== undefined ? ' + typeName + '.byteLength : 4)';
    });

    return { src: src, globalMacros: globalMacros };
  }

  // ---------------------------------------------------------------------------
  // Pass 2: Extract kernels
  // ---------------------------------------------------------------------------

  /**
   * Represents an extracted CUDA kernel.
   */
  function KernelInfo(name, params, body, isDevice) {
    this.name = name;
    this.params = params;     // array of { type, name, isPointer }
    this.body = body;         // raw C++ body string
    this.isDevice = isDevice; // __device__ vs __global__
  }

  /**
   * Parse a C-style parameter list into structured params.
   * e.g. "float* A, const int N, double *B" →
   *   [{ type:'float*', name:'A', isPointer:true }, ...]
   */
  function parseParams(paramStr) {
    if (!paramStr || paramStr.trim().length === 0) return [];
    const parts = [];
    let depth = 0;
    let current = '';
    for (let i = 0; i < paramStr.length; i++) {
      const ch = paramStr[i];
      if (ch === '<' || ch === '(') depth++;
      else if (ch === '>' || ch === ')') depth--;
      else if (ch === ',' && depth === 0) {
        parts.push(current.trim());
        current = '';
        continue;
      }
      current += ch;
    }
    if (current.trim().length > 0) parts.push(current.trim());

    return parts.map(function(p) {
      p = p.trim();
      // Remove qualifiers
      p = p.replace(/\b(const|volatile|__restrict__|restrict)\b/g, '').trim();
      p = p.replace(/\s+/g, ' ');

      // Check for pointer
      const isPointer = p.indexOf('*') !== -1;
      // Extract name — last word token, stripping reference & and pointer *
      const cleanP = p.replace(/[&*]/g, ' ').trim();
      const tokens = cleanP.split(/\s+/);
      let name = tokens[tokens.length - 1].replace(/^[&*]+/, '');
      const type = tokens.slice(0, -1).join(' ');

      const JS_RESERVED = new Set([
        'in', 'default', 'var', 'let', 'const', 'class', 'function', 'new', 'delete',
        'typeof', 'instanceof', 'void', 'this', 'super', 'catch', 'finally', 'do',
        'while', 'for', 'switch', 'case', 'break', 'continue', 'return', 'throw',
        'try', 'with', 'yield', 'await', 'import', 'export', 'enum'
      ]);
      const originalName = name;
      if (JS_RESERVED.has(name)) {
        name = '_' + name;
      }

      return { type: type, name: name, originalName: originalName, isPointer: isPointer };
    });
  }

  /**
   * Find and extract all __global__ and __device__ functions from the source.
   * Returns { kernels: KernelInfo[], deviceFuncs: KernelInfo[], remaining: string }
   */
  function extractKernels(src) {
    const kernels = [];
    const deviceFuncs = [];
    let remaining = src;

    // Match __global__ or __device__ function declarations (supporting templates)
    const funcPattern = /(?:template\s*<[^>]*>\s*)?(__global__|__device__)\s+(?:__launch_bounds__\s*\([^)]*\)\s+)?(?:inline\s+)?(?:void|int|float|double|bool|size_t|auto|\w+)\s*\*?\s*(\w+)\s*\(/g;

    let match;
    const regions = []; // regions to remove from remaining

    while ((match = funcPattern.exec(src)) !== null) {
      const qualifier = match[1];
      const funcName = match[2];
      const parenStart = match.index + match[0].length - 1; // index of '('
      const parenEnd = findMatchingDelimiter(src, parenStart, '(', ')');
      if (parenEnd === -1) continue;

      const paramStr = src.substring(parenStart + 1, parenEnd);

      // Find the opening brace of the function body
      let braceStart = -1;
      for (let j = parenEnd + 1; j < src.length; j++) {
        if (src[j] === '{') { braceStart = j; break; }
        if (src[j] === ';') { braceStart = -1; break; } // forward declaration
        if (!/\s/.test(src[j])) break;
      }
      if (braceStart === -1) continue; // forward declaration or error

      const braceEnd = findMatchingDelimiter(src, braceStart, '{', '}');
      if (braceEnd === -1) continue;

      const body = src.substring(braceStart + 1, braceEnd);
      const params = parseParams(paramStr);

      const info = new KernelInfo(funcName, params, body, qualifier === '__device__');
      if (qualifier === '__global__') {
        kernels.push(info);
      } else {
        deviceFuncs.push(info);
      }

      regions.push({ start: match.index, end: braceEnd + 1 });
    }

    // Remove kernel regions from remaining source (process in reverse to preserve indices)
    regions.sort(function(a, b) { return b.start - a.start; });
    for (let i = 0; i < regions.length; i++) {
      remaining = remaining.substring(0, regions[i].start) + '\n' + remaining.substring(regions[i].end);
    }

    return { kernels: kernels, deviceFuncs: deviceFuncs, remaining: remaining };
  }

  // ---------------------------------------------------------------------------
  // Pass 2b: Transform kernel body
  // ---------------------------------------------------------------------------

  /**
   * Transform a kernel's body from CUDA C++ to JavaScript.
   * Handles threadIdx, blockIdx, shared memory, atomics, pointer access, etc.
   */
  function transformKernelBody(body, params, allKernelAndDeviceNames) {
    let code = body;

    // Rename reserved keyword parameters in kernel body (e.g. in -> _in)
    if (params) {
      for (let pIdx = 0; pIdx < params.length; pIdx++) {
        const p = params[pIdx];
        if (p.originalName && p.originalName !== p.name) {
          code = code.replace(new RegExp('\\b' + p.originalName + '\\b', 'g'), p.name);
        }
      }
    }

    // --- CUDA built-in variable mappings ---
    code = code.replace(/\bthreadIdx\s*\.\s*([xyz])/g, '__tid.$1');
    code = code.replace(/\bblockIdx\s*\.\s*([xyz])/g, '__bid.$1');
    code = code.replace(/\bblockDim\s*\.\s*([xyz])/g, '__bdim.$1');
    code = code.replace(/\bgridDim\s*\.\s*([xyz])/g, '__gdim.$1');

    // __syncthreads() → yield to SIMT scheduler
    code = code.replace(/__syncthreads\s*\(\s*\)/g, 'yield* __sync()');

    // __threadfence() — approximate as sync
    code = code.replace(/__threadfence\s*\(\s*\)/g, 'yield* __sync()');
    code = code.replace(/__threadfence_block\s*\(\s*\)/g, 'yield* __sync()');

    // printf → __printf
    code = code.replace(/\bprintf\s*\(/g, '__printf(');

    // __shared__ declarations
    // Pattern: extern __shared__ type name[]; (dynamic shared memory)
    code = code.replace(/extern\s+__shared__\s+\w+\s+(\w+)\s*\[\s*\]\s*;/g, 'let $1 = __shared;');
    // Pattern: __shared__ type name[d1][d2]; (2D array)
    code = code.replace(/__shared__\s+(\w+)\s+(\w+)\s*\[([^\]]*)\]\s*\[([^\]]*)\]\s*;/g, function(m, type, name, d1, d2) {
      const s1 = d1.trim() || '16';
      const s2 = d2.trim() || '16';
      const t = /int/i.test(type) ? 'int' : 'float';
      return 'let ' + name + ' = __shared.get2DArray ? __shared.get2DArray("' + name + '", ' + s1 + ', ' + s2 + ', "' + t + '") : __shared;';
    });
    // Pattern: __shared__ type name[size]; (1D array)
    code = code.replace(/__shared__\s+(\w+)\s+(\w+)\s*\[([^\]]*)\]\s*;/g, function(m, type, name, size) {
      const s = size.trim() || '0';   // extern __shared__ T name[]: sized by the launch's dynamic shared bytes
      const t = /int/i.test(type) ? 'int' : 'float';
      return 'let ' + name + ' = __shared.getArray ? __shared.getArray("' + name + '", ' + s + ', "' + t + '") : __shared;';
    });

    // Pointer member access: p->field → p.field
    code = code.replace(/->/g, '.');

    // C++ std library and cooperative groups in kernels
    code = code.replace(/\bstd\s*::\s*min\s*\(/g, 'Math.min(');
    code = code.replace(/\bstd\s*::\s*max\s*\(/g, 'Math.max(');
    code = code.replace(/\bstd\s*::\s*abs\s*\(/g, 'Math.abs(');
    code = code.replace(/\bstd\s*::\s*sqrt\s*\(/g, 'Math.sqrt(');
    code = code.replace(/\bassert\s*\([^)]*\)\s*;/g, '/* assert */;');
    code = code.replace(/\b(?:cooperative_groups::)?this_thread_block\s*\(\s*\)/g, '{ sync: function*() { yield* __sync(); } }');
    code = code.replace(/\b(?:cooperative_groups::)?this_grid\s*\(\s*\)/g, '{ sync: function*() { yield* __sync(); } }');
    code = code.replace(/\b(\w+)\.sync\s*\(\s*\)/g, 'yield* __sync()');
    // Pattern: __shared__ type name; (scalar shared variable across block)
    const sharedScalars = new Set();
    const scalarShmemPattern = /__shared__\s+\w+\s+(\w+)\s*;/g;
    let smMatch;
    while ((smMatch = scalarShmemPattern.exec(code)) !== null) {
      sharedScalars.add(smMatch[1]);
    }
    code = code.replace(scalarShmemPattern, '/* __shared__ scalar $1 */');
    for (const sName of sharedScalars) {
      const re = new RegExp('\\b' + sName + '\\b', 'g');
      code = code.replace(re, '__shared.' + sName);
    }

    // Integer division in loops: offset /= 2 → offset = Math.floor(offset / 2)
    code = code.replace(/\b(\w+)\s*\/=\s*(\d+)\b/g, '$1 = Math.floor($1 / $2)');

    // Ceil/warp divisions: (expr) / divisor → Math.floor((expr) / divisor)
    code = code.replace(/\(([a-zA-Z0-9_.]+\s*[+\-*]\s*[a-zA-Z0-9_.]+)\)\s*\/\s*([a-zA-Z0-9_]+)\b/g, 'Math.floor(($1) / $2)');

    // Warp lane/warp id: tid / 32 → Math.floor(tid / 32)
    code = code.replace(/(?<!Math\.floor\()\b(\w+(?:\.\w+)?)\s*\/\s*32\b/g, 'Math.floor($1 / 32)');

    // SIM_SHARED macro
    code = code.replace(/SIM_SHARED\s*\(\s*\w+\s*,\s*(\w+)\s*,\s*[^)]+\)/g, 'let $1 = __shared');

    // --- Atomic operations ---
    // atomicAdd(&ptr[idx], val) → __atomic.add(ptr, idx, val)
    // atomicAdd(ptr + idx, val) → __atomic.add(ptr, idx, val)
    code = replaceAtomicOps(code);

    // --- Pointer/array access transformation ---
    // This is the most critical and complex part.
    // We need to identify which variables are device pointers (kernel params with *)
    // and transform their array access.
    const ptrParams = new Set();
    for (let i = 0; i < params.length; i++) {
      if (params[i].isPointer) ptrParams.add(params[i].name);
    }

    // Identify local pointer variables (e.g. float* r = scores + row * N;)
    // and transform pointer arithmetic: ptr + offset -> ptr.add(offset)
    const localPtrPattern = /(?:const\s+)?(?:float|double|int|char|short|long|unsigned\s+int)\s*\*+\s*(\w+)\s*=\s*([^;]+);/g;
    let lpMatch;
    while ((lpMatch = localPtrPattern.exec(code)) !== null) {
      const varName = lpMatch[1];
      const rhs = lpMatch[2].trim();
      const arithMatch = rhs.match(/^(\w+)\s*([+\-])\s*(.+)$/);
      if (arithMatch) {
        const basePtr = arithMatch[1];
        const op = arithMatch[2];
        const offset = arithMatch[3].trim();
        ptrParams.add(varName);
        const method = op === '+' ? 'add' : 'sub';
        const repl = 'let ' + varName + ' = ' + basePtr + '.' + method + ' ? ' + basePtr + '.' + method + '(' + offset + ') : (' + basePtr + ' ' + op + ' (' + offset + '));';
        code = code.substring(0, lpMatch.index) + repl + code.substring(lpMatch.index + lpMatch[0].length);
        localPtrPattern.lastIndex = lpMatch.index + repl.length;
      } else {
        ptrParams.add(varName);
      }
    }

    code = transformPointerAccess(code, ptrParams);

    // --- Type declarations → let ---
    code = transformTypeDeclarations(code);

    // --- Math functions ---
    code = transformMathFunctions(code);

    // --- Constants ---
    code = transformConstants(code);

    // --- Float literal suffixes ---
    code = code.replace(/(\d+\.?\d*)[fF]\b/g, '$1');
    code = code.replace(/(\d*\.\d+)[fF]\b/g, '$1');

    // --- Type casts ---
    code = transformTypeCasts(code);

    // --- Warp intrinsics (yield to SIMT scheduler) ---
    const warpOps = ['__shfl_down_sync', '__shfl_up_sync', '__shfl_xor_sync', '__shfl_sync', '__ballot_sync', '__all_sync', '__any_sync'];
    for (let o = 0; o < warpOps.length; o++) {
      const op = warpOps[o];
      const re = new RegExp('\\b' + op + '\\s*\\(', 'g');
      let m;
      while ((m = re.exec(code)) !== null) {
        const pStart = m.index + m[0].length - 1;
        const pEnd = findMatchingDelimiter(code, pStart, '(', ')');
        if (pEnd === -1) continue;
        const inner = code.substring(pStart + 1, pEnd);
        const repl = '(yield* this.' + op + '(' + inner + '))';
        code = code.substring(0, m.index) + repl + code.substring(pEnd + 1);
        re.lastIndex = m.index + repl.length;
      }
    }

    // Calls to __device__ functions: prefix with __device_
    for (let i = 0; i < allKernelAndDeviceNames.length; i++) {
      const name = allKernelAndDeviceNames[i];
      const re = new RegExp('\\b' + name + '\\s*\\(', 'g');
      code = code.replace(re, '__device_' + name + '(');
    }

    return code;
  }

  /**
   * Replace atomic operations in kernel code.
   * atomicAdd(&arr[idx], val) → __atomic.add(arr, idx, val)
   * atomicAdd(ptr + idx, val) → __atomic.add(ptr, idx, val)
   */
  function replaceAtomicOps(code) {
    const atomicOps = ['atomicAdd', 'atomicSub', 'atomicMin', 'atomicMax',
                       'atomicAnd', 'atomicOr', 'atomicXor', 'atomicExch',
                       'atomicCAS'];
    const jsOps = ['add', 'sub', 'min', 'max', 'and', 'or', 'xor', 'exch', 'cas'];

    for (let i = 0; i < atomicOps.length; i++) {
      const op = atomicOps[i];
      const jsOp = jsOps[i];
      const re = new RegExp('\\b' + op + '\\s*\\(', 'g');
      let match;
      while ((match = re.exec(code)) !== null) {
        const parenStart = match.index + match[0].length - 1;
        const parenEnd = findMatchingDelimiter(code, parenStart, '(', ')');
        if (parenEnd === -1) continue;

        const inner = code.substring(parenStart + 1, parenEnd).trim();
        const argsResult = splitTopLevelCommas(inner);

        if (argsResult.length >= 2) {
          let firstArg = argsResult[0].trim();
          let remaining = argsResult.slice(1).map(function(a) { return a.trim(); });

          // Parse first arg: &arr[idx] or ptr + idx or &var
          let ptrName, indexExpr;
          const addrOfArray = firstArg.match(/^&\s*(\w+)\s*\[(.+)\]$/) || firstArg.match(/^&\s*(\w+)\s*\.get\((.+)\)$/);
          const addrOfPtrOffset = firstArg.match(/^&?\s*\(?\s*(\w+)\s*\+\s*(.+?)\s*\)?\s*$/);
          const addrOfScalar = firstArg.match(/^&\s*(\w+)$/);

          if (addrOfArray) {
            ptrName = addrOfArray[1];
            indexExpr = addrOfArray[2];
          } else if (addrOfPtrOffset) {
            ptrName = addrOfPtrOffset[1];
            indexExpr = addrOfPtrOffset[2];
            // the lazy regex may have dropped a ')' that belongs to the index expression
            const opens = (indexExpr.match(/\(/g) || []).length, closes = (indexExpr.match(/\)/g) || []).length;
            if (opens > closes) indexExpr += ')'.repeat(opens - closes);
          } else if (addrOfScalar) {
            ptrName = addrOfScalar[1];
            indexExpr = '0';
          } else {
            // Just pass through as-is
            ptrName = firstArg;
            indexExpr = '0';
          }

          const replacement = '__atomic.' + jsOp + '(' + ptrName + ', ' + indexExpr + ', ' + remaining.join(', ') + ')';
          code = code.substring(0, match.index) + replacement + code.substring(parenEnd + 1);
          re.lastIndex = match.index + replacement.length;
        }
      }
    }
    return code;
  }

  /**
   * Split a string on top-level commas (not inside parens/brackets).
   */
  function splitTopLevelCommas(str) {
    const parts = [];
    let depth = 0;
    let current = '';
    for (let i = 0; i < str.length; i++) {
      const ch = str[i];
      if (ch === '(' || ch === '[' || ch === '{') depth++;
      else if (ch === ')' || ch === ']' || ch === '}') depth--;
      else if (ch === ',' && depth === 0) {
        parts.push(current);
        current = '';
        continue;
      }
      current += ch;
    }
    parts.push(current);
    return parts;
  }

  /**
   * Transform pointer/array access in kernel code.
   * For known pointer parameters:
   *   ptr[expr] on RHS → ptr.get(expr)
   *   ptr[expr] = val  → ptr.set(expr, val)
   *   *(ptr + expr)    → ptr.get(expr)
   */
  function transformPointerAccess(code, ptrParams) {
    if (ptrParams.size === 0) return code;

    // Build a regex alternation of pointer parameter names
    const ptrNames = Array.from(ptrParams);
    const ptrPattern = ptrNames.map(function(n) { return n.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }).join('|');

    // Transform vector reinterpret_cast reads & writes:
    // reinterpret_cast<const float4 *>(x)[i] → x.getFloat4(i)
    // reinterpret_cast<float4 *>(y)[i] = v; → y.setFloat4(i, v);
    const vecWritePattern = /(?:reinterpret_cast\s*<\s*(?:const\s+)?(float4|int4|float2|int2)\s*\*+\s*>\s*\(\s*(\w+)\s*\)|\(\s*(?:const\s+)?(float4|int4|float2|int2)\s*\*+\s*\)\s*(\w+))\s*\[([^\]]+)\]\s*=\s*([^;]+);/g;
    code = code.replace(vecWritePattern, function(m, t1, n1, t2, n2, idx, val) {
      const type = t1 || t2;
      const name = n1 || n2;
      const setter = (type.startsWith('float4') || type.startsWith('int4')) ? 'setFloat4' : 'setFloat2';
      return name + '.' + setter + '(' + idx.trim() + ', ' + val.trim() + ');';
    });

    const vecReadPattern = /(?:reinterpret_cast\s*<\s*(?:const\s+)?(float4|int4|float2|int2)\s*\*+\s*>\s*\(\s*(\w+)\s*\)|\(\s*(?:const\s+)?(float4|int4|float2|int2)\s*\*+\s*\)\s*(\w+))\s*\[([^\]]+)\]/g;
    code = code.replace(vecReadPattern, function(m, t1, n1, t2, n2, idx) {
      const type = t1 || t2;
      const name = n1 || n2;
      const getter = (type.startsWith('float4') || type.startsWith('int4')) ? 'getFloat4' : 'getFloat2';
      return name + '.' + getter + '(' + idx.trim() + ')';
    });

    // Transform scalar pointer dereferences:
    // *name = val; or *name += val;
    for (let p = 0; p < ptrNames.length; p++) {
      const name = ptrNames[p];
      const esc = name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

      // A scalar dereference *name MUST be preceded by an operator/delimiter (not operand),
      // and name MUST NOT be followed by '[' (which would be array indexing).
      const derefAssign = new RegExp('(?<=^|[\\s=(,{};:?+\\-!~&|^<>]|\\breturn\\s+)\\*\\s*' + esc + '\\s*(<<=|>>=|[+\\-*\\/%&|^])?=\\s*([^;]+);', 'g');
      code = code.replace(derefAssign, function(m, op, val) {
        if (op) {
          return name + '.set(0, ' + name + '.get(0) ' + op.replace('=', '') + ' (' + val.trim() + '));';
        }
        return name + '.set(0, ' + val.trim() + ');';
      });

      const derefRead = new RegExp('(?<=^|[\\s=(,{};:?+\\-!~&|^<>]|\\breturn\\s+)\\*\\s*' + esc + '\\b(?!\\[)(?!\\s*=)', 'g');
      code = code.replace(derefRead, name + '.get(0)');
    }

    // Transform assignment: ptr[expr] = val → ptr.set(expr, val)
    code = transformPointerAssignments(code, ptrNames);

    // Transform reads: ptr[expr] → ptr.get(expr) (for remaining occurrences)
    code = transformPointerReads(code, ptrNames);

    // Transform *(ptr + expr) → ptr.get(expr)
    const derefPattern = new RegExp('\\*\\s*\\(\\s*(' + ptrPattern + ')\\s*\\+\\s*([^)]+)\\)', 'g');
    code = code.replace(derefPattern, function(m, name, offset) {
      return name + '.get(' + offset.trim() + ')';
    });

    return code;
  }

  /**
   * Transform ptr[expr] = val and ptr[expr] op= val assignments (including multi-line).
   */
  function transformPointerAssignments(code, ptrNames) {
    for (let p = 0; p < ptrNames.length; p++) {
      const name = ptrNames[p];
      const escaped = name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      const assignPattern = new RegExp('\\b' + escaped + '\\s*\\[', 'g');
      let m;
      while ((m = assignPattern.exec(code)) !== null) {
        const bracketStart = m.index + m[0].length - 1;
        const bracketEnd = findMatchingDelimiter(code, bracketStart, '[', ']');
        if (bracketEnd === -1) continue;

        const indexExpr = code.substring(bracketStart + 1, bracketEnd).trim();
        const afterBracket = code.substring(bracketEnd + 1);

        const leadingWsMatch = afterBracket.match(/^\s*/);
        const wsLen = leadingWsMatch ? leadingWsMatch[0].length : 0;
        const trimmedAfter = afterBracket.substring(wsLen);

        // Check for compound assignment: +=, -=, *=, /=, |=, &=, ^=, <<=, >>=, %=
        const compoundMatch = trimmedAfter.match(/^(<<=|>>=|[+\-*/%&|^])=\s*/);
        if (compoundMatch) {
          const op = compoundMatch[1];
          const afterOp = trimmedAfter.substring(compoundMatch[0].length);
          const semiIdx = findStatementEnd(afterOp);
          const valExpr = afterOp.substring(0, semiIdx).trim();

          const totalLen = (bracketEnd + 1 + wsLen + compoundMatch[0].length + semiIdx + 1) - m.index;
          const replacement = name + '.set(' + indexExpr + ', ' + name + '.get(' + indexExpr + ') ' + op + ' (' + valExpr + '));';

          code = code.substring(0, m.index) + replacement + code.substring(m.index + totalLen);
          assignPattern.lastIndex = m.index + replacement.length;
          continue;
        }

        // Check for simple assignment: = value
        const simpleMatch = trimmedAfter.match(/^=\s*/);
        if (simpleMatch) {
          const afterEq = trimmedAfter.substring(simpleMatch[0].length);
          const semiIdx = findStatementEnd(afterEq);
          const valExpr = afterEq.substring(0, semiIdx).trim();

          const totalLen = (bracketEnd + 1 + wsLen + simpleMatch[0].length + semiIdx + 1) - m.index;
          const replacement = name + '.set(' + indexExpr + ', ' + valExpr + ');';

          code = code.substring(0, m.index) + replacement + code.substring(m.index + totalLen);
          assignPattern.lastIndex = m.index + replacement.length;
          continue;
        }

        // Check for ++ or --
        const incDecMatch = trimmedAfter.match(/^(\+\+|--)\s*;/);
        if (incDecMatch) {
          const op = incDecMatch[1] === '++' ? '+' : '-';
          const totalLen = (bracketEnd + 1 + wsLen + incDecMatch[0].length) - m.index;
          const replacement = name + '.set(' + indexExpr + ', ' + name + '.get(' + indexExpr + ') ' + op + ' 1);';

          code = code.substring(0, m.index) + replacement + code.substring(m.index + totalLen);
          assignPattern.lastIndex = m.index + replacement.length;
          continue;
        }
      }
    }
    return code;
  }

  /**
   * Find the end of a statement expression (the position of the ';' or end of line).
   * Respects nested parens/brackets.
   */
  function findStatementEnd(str) {
    let depth = 0;
    for (let i = 0; i < str.length; i++) {
      const ch = str[i];
      if (ch === '(' || ch === '[' || ch === '{') depth++;
      else if (ch === ')' || ch === ']' || ch === '}') depth--;
      else if (ch === ';' && depth === 0) return i;
    }
    return str.length;
  }

  /**
   * Transform ptr[expr] reads → ptr.get(expr) for known pointer params.
   * Must run AFTER assignment transforms so we don't double-transform.
   */
  function transformPointerReads(code, ptrNames) {
    for (let p = 0; p < ptrNames.length; p++) {
      const name = ptrNames[p];
      const escaped = name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

      // Replace name[expr] with name.get(expr) — but only if not already .set(
      const pattern = new RegExp('\\b' + escaped + '\\[', 'g');
      let m;
      let result = '';
      let lastIdx = 0;

      while ((m = pattern.exec(code)) !== null) {
        const bracketStart = m.index + m[0].length - 1;
        const bracketEnd = findMatchingDelimiter(code, bracketStart, '[', ']');
        if (bracketEnd === -1) continue;

        const indexExpr = code.substring(bracketStart + 1, bracketEnd);
        result += code.substring(lastIdx, m.index);
        result += name + '.get(' + indexExpr + ')';
        lastIdx = bracketEnd + 1;
        pattern.lastIndex = bracketEnd + 1;
      }
      result += code.substring(lastIdx);
      code = result;
    }
    return code;
  }

  // ---------------------------------------------------------------------------
  // Type declaration transformations (shared between kernel & host)
  // ---------------------------------------------------------------------------

  /**
   * Transform C/C++ type declarations to JS let/const.
   */
  function transformTypeDeclarations(code) {
    // Pointer array declarations: type* name[size]; or type *name[size];
    const ptrArrayPattern = /(?:const\s+)?(?:float|double|int|unsigned\s+int|short|char|long|size_t|void|cudaStream_t|ncclComm_t|cudaEvent_t|\w+)\s*\*+\s*(\w+)\s*\[([^\]]+)\]\s*;/g;
    code = code.replace(ptrArrayPattern, function(m, name, size) {
      return 'let ' + name + ' = new Array(Math.max(16, ' + size.trim() + ')).fill(null);';
    });

    // Handle special multi-gpu handle arrays: cudaStream_t streams[2]; ncclComm_t comms[2]; etc.
    code = code.replace(/\b(?:cudaStream_t|ncclComm_t|cudaEvent_t)\s+(\w+)\s*\[([^\]]+)\]\s*;/g, function(m, name, size) {
      return 'let ' + name + ' = new Array(Math.max(16, ' + size.trim() + ')).fill(null);';
    });

    // std::vector declarations
    code = code.replace(/\bstd\s*::\s*vector\s*<[^>]+>\s*(\w+)\s*\(\s*([^,)]+)(?:\s*,\s*([^)]+))?\s*\)\s*;/g, function(m, name, size, initVal) {
      const val = initVal ? initVal.trim() : '0';
      return 'let ' + name + ' = new Array(' + size.trim() + ').fill(' + val + ');';
    });
    code = code.replace(/\bstd\s*::\s*vector\s*<[^>]+>\s*(\w+)\s*;/g, 'let $1 = [];');

    // Reference declarations: type &name = expr; or type& name = expr;
    code = code.replace(/(?:const\s+)?(?:float|double|int|unsigned\s+int|short|char|long|size_t|auto|\w+)\s*&+\s*(\w+)\s*=/g, 'let $1 =');

    // Multi-dimensional pointer array declarations: type* name[d1][d2]; or type *name[d1][d2];
    const ptrMultiDimPattern = /(?:const\s+)?(?:float|double|int|unsigned\s+int|short|char|long|size_t|void|cudaStream_t|ncclComm_t|cudaEvent_t|\w+)\s*\*+\s*(\w+)\s*((?:\[[^\]]*\]){2,})\s*;/g;
    code = code.replace(ptrMultiDimPattern, function(m, name, dimsStr) {
      const dims = [];
      const dimRegex = /\[([^\]]*)\]/g;
      let dm;
      while ((dm = dimRegex.exec(dimsStr)) !== null) dims.push(dm[1].trim());
      const d0 = dims[0] && dims[0].length > 0 ? dims[0] : '16';
      const d1 = dims[1] && dims[1].length > 0 ? dims[1] : '16';
      return 'let ' + name + ' = Array.from({length: Math.max(16, typeof ' + d0 + ' !== "undefined" ? ' + d0 + ' : 16)}, function() { return new Array(Math.max(16, typeof ' + d1 + ' !== "undefined" ? ' + d1 + ' : 16)).fill(null); });';
    });

    // Multi-dimensional array declarations: type name[dim1][dim2]... (= { ... })?;
    const multiDimDeclPattern = /(?:const\s+)?(float|double|int|unsigned\s+int|short|char|unsigned\s+char|long|long\s+long|size_t|uint64_t|int64_t|uint32_t|int32_t|uint16_t|int16_t|uint8_t|int8_t|bool)\s+(\w+)\s*((?:\[[^\]]*\]){2,})\s*(?:=\s*(\{[\s\S]*?\}))?\s*;/g;
    code = code.replace(multiDimDeclPattern, function(match, type, name, dimsStr, initBlock) {
      let typedArrayType = 'Float32Array';
      if (type === 'double') typedArrayType = 'Float64Array';
      else if (type === 'int' || type === 'long' || type === 'int32_t' || type === 'long long') typedArrayType = 'Int32Array';
      else if (type === 'unsigned int' || type === 'size_t' || type === 'uint32_t' || type === 'uint64_t') typedArrayType = 'Uint32Array';
      else if (type === 'short' || type === 'int16_t') typedArrayType = 'Int16Array';
      else if (type === 'char' || type === 'int8_t') typedArrayType = 'Int8Array';
      else if (type === 'unsigned char' || type === 'uint8_t') typedArrayType = 'Uint8Array';

      const dims = [];
      const dimRegex = /\[([^\]]*)\]/g;
      let dm;
      while ((dm = dimRegex.exec(dimsStr)) !== null) dims.push(dm[1].trim());

      const d0 = dims[0] && dims[0].length > 0 ? dims[0] : '16';
      const d1 = dims[1] && dims[1].length > 0 ? dims[1] : '16';

      if (initBlock !== undefined && initBlock.trim().length > 0) {
        let jsInit = initBlock.trim()
          .replace(/(\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)f\b/g, '$1')
          .replace(/\{/g, '[')
          .replace(/\}/g, ']');

        return 'let ' + name + ' = (function() {\n' +
               '  const __init = (' + jsInit + ').map(function(__r) { return Array.isArray(__r) ? new ' + typedArrayType + '(__r) : __r; });\n' +
               '  const __rows = Math.max(16, typeof ' + d0 + ' !== "undefined" ? ' + d0 + ' : __init.length);\n' +
               '  const __cols = Math.max(16, typeof ' + d1 + ' !== "undefined" ? ' + d1 + ' : 16);\n' +
               '  const __res = [];\n' +
               '  for (let __i = 0; __i < __rows; __i++) {\n' +
               '    __res.push(__i < __init.length ? __init[__i] : new ' + typedArrayType + '(__cols));\n' +
               '  }\n' +
               '  return __res;\n' +
               '})();';
      }

      return 'let ' + name + ' = Array.from({length: Math.max(16, typeof ' + d0 + ' !== "undefined" ? ' + d0 + ' : 16)}, function() { return new ' + typedArrayType + '(Math.max(16, typeof ' + d1 + ' !== "undefined" ? ' + d1 + ' : 16)); });';
    });

    // Array declarations: type name[size]; or type name[size] = {...};
    const arrayDeclPattern = /(?:const\s+)?(float|double|int|unsigned\s+int|short|char|unsigned\s+char|long|long\s+long|size_t|uint64_t|int64_t|uint32_t|int32_t|uint16_t|int16_t|uint8_t|int8_t|bool)\s+(\w+)\s*\[([^\]]*)\](?:\s*=\s*\{([^}]*)\})?\s*;/g;
    code = code.replace(arrayDeclPattern, function(match, type, name, size, initValues) {
      let typedArrayType = 'Float32Array';
      if (type === 'double') typedArrayType = 'Float64Array';
      else if (type === 'int' || type === 'long' || type === 'int32_t' || type === 'long long') typedArrayType = 'Int32Array';
      else if (type === 'unsigned int' || type === 'size_t' || type === 'uint32_t' || type === 'uint64_t') typedArrayType = 'Uint32Array';
      else if (type === 'short' || type === 'int16_t') typedArrayType = 'Int16Array';
      else if (type === 'char' || type === 'int8_t') typedArrayType = 'Int8Array';
      else if (type === 'unsigned char' || type === 'uint8_t') typedArrayType = 'Uint8Array';

      if (initValues !== undefined && initValues.trim().length > 0) {
        let cleanInit = initValues.trim().replace(/(\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)f\b/g, '$1');
        return 'let ' + name + ' = new ' + typedArrayType + '([' + cleanInit + ']);';
      }
      const s = size && size.trim().length > 0 ? size.trim() : '16';
      return 'let ' + name + ' = new ' + typedArrayType + '(typeof (' + s + ') !== "undefined" ? (' + s + ') : 16);';
    });

    // List of C types to strip (order matters — longest first)
    const cTypes = [
      'cudaError_t', 'cudaError', 'cudaStream_t', 'cudaEvent_t', 'cudaDeviceProp',
      'ncclComm_t', 'ncclUniqueId', 'ncclResult_t',
      'unsigned long long', 'unsigned long', 'unsigned int', 'unsigned short', 'unsigned char',
      'long long', 'long double',
      'size_t', 'uint64_t', 'int64_t', 'uint32_t', 'int32_t', 'uint16_t', 'int16_t', 'uint8_t', 'int8_t',
      'ptrdiff_t', 'ssize_t',
      'float4', 'float3', 'float2', 'int4', 'int3', 'int2', 'double2',
      'float', 'double', 'int', 'short', 'char', 'long', 'bool', 'void', 'auto'
    ];

    // Integer declarations with division: int/size_t/uint x = expr_with_division;
    code = code.replace(/(?:const\s+)?\b(int|size_t|unsigned\s+int|uint32_t|int32_t|short|long)\s+(\w+)\s*=\s*([^;]+);/g, function(m, type, name, expr) {
      const trimmed = expr.trim();
      if (trimmed.includes('/') && !trimmed.startsWith('Math.floor(')) {
        return 'let ' + name + ' = Math.floor(' + trimmed + ');';
      }
      return 'let ' + name + ' = ' + trimmed + ';';
    });

    for (let t = 0; t < cTypes.length; t++) {
      const type = cTypes[t];
      const escaped = type.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

      // const type * name → const name  (or let name for non-const)
      // type * name = ... → let name = ...
      // type name = ... → let name = ...
      // type name; → let name;

      // Handle pointer declarations: type* name or type *name
      const ptrDecl = new RegExp('(^|[;{}\\n(])(\\s*)(const\\s+)?' + escaped + '\\s*\\*+\\s*(\\w+)', 'gm');
      code = code.replace(ptrDecl, function(match, pre, ws, constKw, varName) {
        const kw = constKw ? 'const ' : 'let ';
        return pre + ws + kw + varName;
      });

      // Handle reference declarations: type &name or type& name
      const refDecl = new RegExp('(^|[;{}\\n(])(\\s*)(const\\s+)?' + escaped + '\\s*&+\\s*(\\w+)', 'gm');
      code = code.replace(refDecl, function(match, pre, ws, constKw, varName) {
        const kw = constKw ? 'const ' : 'let ';
        return pre + ws + kw + varName;
      });

      // Handle non-pointer declarations: type name
      // Be careful not to match inside words (e.g., "float" in "floatValue")
      const valDecl = new RegExp('(^|[;{}\\n(])(\\s*)(const\\s+)?(static\\s+)?' + escaped + '\\s+(\\w+)', 'gm');
      code = code.replace(valDecl, function(match, pre, ws, constKw, staticKw, varName) {
        // Don't transform function return types — skip if followed by (
        const kw = constKw ? 'const ' : 'let ';
        return pre + ws + kw + varName;
      });
    }

    // Clean up multiple pointer declarations on a single line: "let a, *b, *c;" -> "let a, b, c;"
    code = code.replace(/(\blet\s+[^;]+);/g, function(match, decl) {
      return decl.replace(/,\s*\*+/g, ', ') + ';';
    });

    // Clean up: "let let" → "let", "const const" → "const"
    code = code.replace(/\blet\s+let\b/g, 'let');
    code = code.replace(/\bconst\s+const\b/g, 'const');
    code = code.replace(/\blet\s+const\b/g, 'const');

    // Strip & from any let/const/var declaration (e.g. let &ref -> let ref)
    code = code.replace(/\b(let|const|var)\s*&+\s*(\w+)/g, '$1 $2');

    // Universal safety pass: ensure no "let/const name[...]" remains in JS output
    code = code.replace(/\b(let|const)\s+(\w+)\s*((?:\[[^\]]*\])+)(?:\s*=\s*(\{[\s\S]*?\}|[^;]+))?\s*;/g, function(m, kw, name, dimsStr, initVal) {
      const dims = [];
      const dimRegex = /\[([^\]]*)\]/g;
      let dm;
      while ((dm = dimRegex.exec(dimsStr)) !== null) dims.push(dm[1].trim());

      const d0 = dims[0] && dims[0].length > 0 ? dims[0] : '16';
      if (dims.length === 1) {
        if (initVal) {
          let cleanInit = initVal.trim().replace(/^\{|\}$/g, '').replace(/(\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)f\b/g, '$1');
          return 'let ' + name + ' = new Float32Array([' + cleanInit + ']);';
        }
        return 'let ' + name + ' = new Float32Array(typeof (' + d0 + ') !== "undefined" ? (' + d0 + ') : 16);';
      }
      const d1 = dims[1] && dims[1].length > 0 ? dims[1] : '16';
      if (initVal) {
        let jsInit = initVal.trim().replace(/(\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)f\b/g, '$1').replace(/\{/g, '[').replace(/\}/g, ']');
        return 'let ' + name + ' = (function() {\n' +
               '  const __init = (' + jsInit + ').map(function(__r) { return Array.isArray(__r) ? new Float32Array(__r) : __r; });\n' +
               '  const __rows = Math.max(16, typeof ' + d0 + ' !== "undefined" ? ' + d0 + ' : __init.length);\n' +
               '  const __cols = Math.max(16, typeof ' + d1 + ' !== "undefined" ? ' + d1 + ' : 16);\n' +
               '  const __res = [];\n' +
               '  for (let __i = 0; __i < __rows; __i++) {\n' +
               '    __res.push(__i < __init.length ? __init[__i] : new Float32Array(__cols));\n' +
               '  }\n' +
               '  return __res;\n' +
               '})();';
      }
      return 'let ' + name + ' = Array.from({length: Math.max(16, typeof ' + d0 + ' !== "undefined" ? ' + d0 + ' : 16)}, function() { return new Float32Array(Math.max(16, typeof ' + d1 + ' !== "undefined" ? ' + d1 + ' : 16)); });';
    });

    return code;
  }

  // ---------------------------------------------------------------------------
  // Math function transformations
  // ---------------------------------------------------------------------------

  /**
   * Transform CUDA/C math function calls to JavaScript equivalents.
   */
  function transformMathFunctions(code) {
    const funcNames = Object.keys(MATH_FUNCS);
    // Sort by length descending to match longer names first (e.g., __expf before exp)
    funcNames.sort(function(a, b) { return b.length - a.length; });

    for (let i = 0; i < funcNames.length; i++) {
      const name = funcNames[i];
      const info = MATH_FUNCS[name];
      // Only match standalone function calls — not part of another identifier
      // Use negative lookbehind/lookahead for word boundaries
      const pattern = new RegExp('\\b' + name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\s*\\(', 'g');

      let m;
      while ((m = pattern.exec(code)) !== null) {
        // Verify it's not part of a larger identifier
        if (m.index > 0 && /\w/.test(code[m.index - 1]) && !name.startsWith('__')) continue;
        // Verify it's not already preceded by "Math."
        if (m.index >= 5 && code.substring(m.index - 5, m.index) === 'Math.') continue;

        const parenStart = m.index + m[0].length - 1;
        const parenEnd = findMatchingDelimiter(code, parenStart, '(', ')');
        if (parenEnd === -1) continue;

        const argStr = code.substring(parenStart + 1, parenEnd);
        const args = splitTopLevelCommas(argStr).map(function(a) { return a.trim(); });

        let replacement;
        if (info.js) {
          replacement = info.js + '(' + args.join(', ') + ')';
        } else if (info.template) {
          replacement = info.template;
          for (let a = 0; a < args.length; a++) {
            replacement = replacement.split('$' + (a + 1)).join(args[a]);
          }
        } else {
          continue;
        }

        code = code.substring(0, m.index) + replacement + code.substring(parenEnd + 1);
        pattern.lastIndex = m.index + replacement.length;
      }
    }
    return code;
  }

  // ---------------------------------------------------------------------------
  // Constant transformations
  // ---------------------------------------------------------------------------

  function transformConstants(code) {
    const names = Object.keys(CONSTANT_MAP);
    for (let i = 0; i < names.length; i++) {
      const name = names[i];
      const escaped = name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      const pattern = new RegExp('\\b' + escaped + '\\b', 'g');
      code = code.replace(pattern, CONSTANT_MAP[name]);
    }
    return code;
  }

  // ---------------------------------------------------------------------------
  // Type cast transformations
  // ---------------------------------------------------------------------------

  function transformTypeCasts(code) {
    // (size_t), (uint64_t), (int64_t), (uint32_t), (int32_t), (long), (long long), (short), (char) → strip
    code = code.replace(/\(\s*(?:size_t|uint64_t|int64_t|uint32_t|int32_t|short|long|long\s+long)\s*\)\s*/g, '');

    // (int)expr → (expr|0)  — integer truncation
    // (int)x, (int)(a*b), (unsigned int)(...): the operand may be a parenthesised expression
    const castRe = /\(\s*(int|unsigned\s+int|unsigned)\s*\)\s*/g;
    let cm;
    while ((cm = castRe.exec(code)) !== null) {
      const operandEnd = atomForward(code, cm.index + cm[0].length);
      if (operandEnd < 0) continue;
      const operand = code.slice(cm.index + cm[0].length, operandEnd);
      const rep = cm[1] === 'int' ? 'Math.trunc(' + operand + ')' : '((' + operand + ')>>>0)';
      code = code.slice(0, cm.index) + rep + code.slice(operandEnd);
      castRe.lastIndex = cm.index + rep.length;
    }

    // (float)expr, (double)expr → just (expr)
    code = code.replace(/\(\s*(?:float|double)\s*\)\s*/g, '');

    // (float*), (int*), (void*), (char*), (void**) etc → strip
    code = code.replace(/\(\s*(?:const\s+)?(?:float|double|int|unsigned\s+int|char|void|short|long|long\s+long|size_t|uint8_t|uint32_t)\s*\*+\s*\)/g, '');

    // static_cast<type>(expr) → (expr)
    code = code.replace(/static_cast\s*<[^>]+>\s*\(/g, '(');
    // reinterpret_cast, const_cast — same treatment
    code = code.replace(/reinterpret_cast\s*<[^>]+>\s*\(/g, '(');
    code = code.replace(/const_cast\s*<[^>]+>\s*\(/g, '(');

    return code;
  }

  // ---------------------------------------------------------------------------
  // Pass 3: Transform host code
  // ---------------------------------------------------------------------------

  /**
   * Transform the host portion of the CUDA source (main function and global scope).
   */
  function transformHostCode(src, kernelNames, warnings) {
    let code = src;

    // Strip extern "C" first (accounting for protected string tokens)
    code = code.replace(/\bextern\s+(?:"C"|__STR_\w+__)\s*\{/g, '{');
    code = code.replace(/\bextern\s+(?:"C"|__STR_\w+__)\s*/g, '');
    code = code.replace(/\bextern\b\s*/g, '');

    // --- Transform host function declarations (outside main) into JS functions ---
    // Pattern: [extern "C"] [inline] returnType funcName(params) {
    const hostFuncPattern = /(?:extern\s+"C"\s+)?(?:inline\s+)?(?:void|int|float|double|bool|size_t|\w+)\s+(\w+)\s*\(/g;
    let hfMatch;
    while ((hfMatch = hostFuncPattern.exec(code)) !== null) {
      const fName = hfMatch[1];
      if (fName === 'main' || fName === 'if' || fName === 'for' || fName === 'while' || fName === 'switch' || fName === 'catch') continue;
      const parenStart = hfMatch.index + hfMatch[0].length - 1;
      const parenEnd = findMatchingDelimiter(code, parenStart, '(', ')');
      if (parenEnd === -1) continue;

      // Ensure this is followed by { (a function definition, not a call or prototype)
      let braceStart = -1;
      for (let j = parenEnd + 1; j < code.length; j++) {
        if (code[j] === '{') { braceStart = j; break; }
        if (code[j] === ';') { braceStart = -1; break; }
        if (!/\s/.test(code[j])) break;
      }
      if (braceStart === -1) continue;

      const paramStr = code.substring(parenStart + 1, parenEnd);
      const params = parseParams(paramStr);
      const paramNames = params.map(function(p) { return p.name; }).join(', ');

      const repl = 'function ' + fName + '(' + paramNames + ')';
      code = code.substring(0, hfMatch.index) + repl + code.substring(parenEnd + 1);
      hostFuncPattern.lastIndex = hfMatch.index + repl.length;
    }

    // --- Extract main() body ---
    // Find: int main(...) { ... }  or  void main(...) { ... }
    const mainMatch = code.match(/\b(?:int|void)\s+main\s*\([^)]*\)\s*\{/);
    if (mainMatch) {
      const braceStart = code.indexOf('{', mainMatch.index + mainMatch[0].length - 1);
      const braceEnd = findMatchingDelimiter(code, braceStart, '{', '}');
      if (braceEnd !== -1) {
        const beforeMain = code.substring(0, mainMatch.index);
        const mainBody = code.substring(braceStart + 1, braceEnd);
        const afterMain = code.substring(braceEnd + 1);
        // Combine: code outside main + main body (but skip "return 0;" at end)
        code = beforeMain + '\n' + mainBody + '\n' + afterMain;
      }
    }

    // Strip "return 0;" or "return EXIT_SUCCESS;"
    code = code.replace(/\breturn\s+0\s*;/g, '');
    code = code.replace(/\breturn\s+EXIT_SUCCESS\s*;/g, '');

    // --- Kernel launches ---
    // kernel<<<grid, block>>>(args)  →  __rt.launch(__kernel_kernel, grid, block, 0, args)
    // kernel<<<grid, block, shmem>>>(args)  →  __rt.launch(__kernel_kernel, grid, block, shmem, args)
    // kernel<TEMPLATE><<<grid, block>>>(args)  →  same (strip template)
    code = transformKernelLaunches(code, kernelNames, warnings);

    // --- cudaMalloc ---
    // Handles &ptr, &ptr[i], (void**)&ptr, (float**)&ptr[i], etc.
    code = code.replace(/cudaMalloc\s*\(\s*(?:\([^)]*\)\s*)?&?\s*(?:\([^)]*\)\s*)?([\w.\[\]]+)\s*,\s*([^)]+)\)/g,
      function(m, name, size) {
        return name.trim() + ' = __rt.cudaMalloc(' + size.trim() + ')';
      });

    // --- cudaMallocHost / cudaHostAlloc ---
    code = code.replace(/cuda(?:MallocHost|HostAlloc)\s*\(\s*(?:\([^)]*\)\s*)?&?\s*(?:\([^)]*\)\s*)?([\w.\[\]]+)\s*,\s*([^)]+)\)/g,
      function(m, name, size) {
        return name.trim() + ' = new Float32Array(Math.floor((' + size.trim() + ') / 4))';
      });
    code = code.replace(/cudaFreeHost\s*\([^)]*\)/g, '/* host freed */');

    // --- cudaEvent timing APIs ---
    code = code.replace(/cudaEventElapsedTime\s*\(\s*&?\s*([\w.\[\]]+)[^)]*\)/g, '$1 = (__rt.getCounters().estimatedTimeMs || 0.12)');
    code = code.replace(/cudaEventCreate\s*\([^)]*\)/g, '/* event created */');
    code = code.replace(/cudaEventRecord\s*\([^)]*\)/g, '/* event recorded */');
    code = code.replace(/cudaEventSynchronize\s*\([^)]*\)/g, '__rt.cudaDeviceSynchronize()');
    code = code.replace(/cudaEventDestroy\s*\([^)]*\)/g, '/* event destroyed */');

    // --- cudaMemcpyToSymbol / cudaMemcpyFromSymbol ---
    code = code.replace(/cudaMemcpyToSymbol\s*\(\s*(\w+)\s*,\s*([^,]+)\s*,\s*([^)]+)\)/g, '__rt.cudaMemcpy($1, $2, $3, "H2D")');
    code = code.replace(/cudaMemcpyFromSymbol\s*\(\s*([^,]+)\s*,\s*(\w+)\s*,\s*([^)]+)\)/g, '__rt.cudaMemcpy($1, $2, $3, "D2H")');

    // --- Struct definitions and member access in host ---
    const userStructs = new Set();
    const structDefPattern = /\bstruct\s+(\w+)\s*\{([^}]*)\}\s*;/g;
    let sMatch;
    while ((sMatch = structDefPattern.exec(code)) !== null) {
      userStructs.add(sMatch[1]);
    }
    code = code.replace(structDefPattern, 'function $1(init) { Object.assign(this, init || {}); };');
    for (const sName of userStructs) {
      // struct Point* p = ... or Point* p = &var;
      code = code.replace(new RegExp('(?:struct\\s+)?' + sName + '\\s*\\*+\\s*(\\w+)\\s*=\\s*&?(\\w+)\\s*;', 'g'), 'let $1 = $2;');
      code = code.replace(new RegExp('(?:struct\\s+)?' + sName + '\\s*\\*+\\s*(\\w+)', 'g'), 'let $1');
      // struct Point p; or Point p;
      code = code.replace(new RegExp('(?:struct\\s+)?' + sName + '\\s+(\\w+)\\s*;', 'g'), 'let $1 = new ' + sName + '();');
      code = code.replace(new RegExp('(?:struct\\s+)?' + sName + '\\s+(\\w+)\\s*=', 'g'), 'let $1 =');
    }
    code = code.replace(/->/g, '.');

    // --- C++ std library and random in host ---
    code = code.replace(/\bstd\s*::\s*min\s*\(/g, 'Math.min(');
    code = code.replace(/\bstd\s*::\s*max\s*\(/g, 'Math.max(');
    code = code.replace(/\bstd\s*::\s*abs\s*\(/g, 'Math.abs(');
    code = code.replace(/\bstd\s*::\s*sqrt\s*\(/g, 'Math.sqrt(');
    code = code.replace(/\bstd\s*::\s*swap\s*\(\s*([^,]+)\s*,\s*([^)]+)\)/g, '([$1, $2] = [$2, $1])');
    code = code.replace(/\bassert\s*\([^)]*\)\s*;/g, '/* assert */;');
    code = code.replace(/\bassert\b\s*\(/g, '/* assert */ (');
    code = code.replace(/\brand\s*\(\s*\)\s*%\s*(\d+)/g, 'Math.floor(Math.random() * $1)');
    code = code.replace(/\brand\s*\(\s*\)\s*\/\s*\(\s*(?:float|double)\s*\)\s*RAND_MAX/g, 'Math.random()');
    code = code.replace(/\brand\s*\(\s*\)/g, 'Math.floor(Math.random() * 32768)');
    code = code.replace(/\bsrand\s*\([^)]*\)\s*;/g, '/* srand */');
    code = code.replace(/\bexit\s*\([^)]*\)\s*;/g, 'return;');

    // --- cudaFree ---
    code = code.replace(/cudaFree\s*\(\s*([\w.\[\]]+)\s*\)/g, '__rt.cudaFree($1)');

    // --- cudaMemcpy (scalar & array) ---
    // cudaMemcpy(dst, src + offset, size, kind) -> subarray slice
    code = code.replace(/cudaMemcpy\s*\(\s*([^,]+),\s*([\w]+)\s*\+\s*([^,]+),\s*([^,]+),\s*cudaMemcpyHostToDevice\s*\)/g,
      function(m, dst, src, offset, size) {
        return '__rt.cudaMemcpy(' + dst.trim() + ', ' + src.trim() + '.subarray ? ' + src.trim() + '.subarray(' + offset.trim() + ') : ' + src.trim() + ', ' + size.trim() + ", 'H2D')";
      });

    // cudaMemcpy(dst + offset, src, size, kind) -> subarray slice
    code = code.replace(/cudaMemcpy\s*\(\s*([\w]+)\s*\+\s*([^,]+),\s*([^,]+),\s*([^,]+),\s*cudaMemcpyDeviceToHost\s*\)/g,
      function(m, dst, offset, src, size) {
        return '__rt.cudaMemcpy(' + dst.trim() + '.subarray ? ' + dst.trim() + '.subarray(' + offset.trim() + ') : ' + dst.trim() + ', ' + src.trim() + ', ' + size.trim() + ", 'D2H')";
      });

    // cudaMemcpy(d_ptr, &src_arr[offset], size, cudaMemcpyHostToDevice) -> subarray slice
    code = code.replace(/cudaMemcpy\s*\(\s*([^,]+),\s*&\s*([\w]+)\[([^\]]+)\]\s*,\s*([^,]+),\s*cudaMemcpyHostToDevice\s*\)/g,
      function(m, dst, src, offset, size) {
        return '__rt.cudaMemcpy(' + dst.trim() + ', ' + src.trim() + '.subarray ? ' + src.trim() + '.subarray(' + offset.trim() + ') : ' + src.trim() + ', ' + size.trim() + ", 'H2D')";
      });

    // cudaMemcpy(&dst, src, size, cudaMemcpyDeviceToHost) -> dst = __rt.cudaMemcpyD2H_Scalar(src, size)
    code = code.replace(/cudaMemcpy\s*\(\s*&\s*([\w.\[\]]+)\s*,\s*([^,]+),\s*([^,]+),\s*cudaMemcpyDeviceToHost\s*\)/g,
      function(m, dst, src, size) {
        return dst.trim() + ' = __rt.cudaMemcpyD2H_Scalar(' + src.trim() + ', ' + size.trim() + ')';
      });

    // cudaMemcpy(dst, &src, size, cudaMemcpyHostToDevice) -> __rt.cudaMemcpyH2D_Scalar(dst, src, size)
    code = code.replace(/cudaMemcpy\s*\(\s*([^,]+),\s*&\s*([\w.\[\]]+)\s*,\s*([^,]+),\s*cudaMemcpyHostToDevice\s*\)/g,
      function(m, dst, src, size) {
        return '__rt.cudaMemcpyH2D_Scalar(' + dst.trim() + ', ' + src.trim() + ', ' + size.trim() + ')';
      });

    // cudaMemcpy(dst, src, size, cudaMemcpyHostToDevice) → __rt.cudaMemcpy(dst, src, size, 'H2D')
    code = code.replace(/cudaMemcpy\s*\(\s*([^,]+),\s*([^,]+),\s*([^,]+),\s*cudaMemcpyHostToDevice\s*\)/g,
      function(m, dst, src, size) {
        return '__rt.cudaMemcpy(' + dst.trim() + ', ' + src.trim() + ', ' + size.trim() + ", 'H2D')";
      });
    code = code.replace(/cudaMemcpy\s*\(\s*([^,]+),\s*([^,]+),\s*([^,]+),\s*cudaMemcpyDeviceToHost\s*\)/g,
      function(m, dst, src, size) {
        return '__rt.cudaMemcpy(' + dst.trim() + ', ' + src.trim() + ', ' + size.trim() + ", 'D2H')";
      });
    code = code.replace(/cudaMemcpy\s*\(\s*([^,]+),\s*([^,]+),\s*([^,]+),\s*cudaMemcpyDeviceToDevice\s*\)/g,
      function(m, dst, src, size) {
        return '__rt.cudaMemcpy(' + dst.trim() + ', ' + src.trim() + ', ' + size.trim() + ", 'D2D')";
      });

    // --- cudaMemset ---
    code = code.replace(/cudaMemset\s*\(\s*([^,]+),\s*([^,]+),\s*([^)]+)\)/g,
      function(m, ptr, val, size) {
        return '__rt.cudaMemset(' + ptr.trim() + ', ' + val.trim() + ', ' + size.trim() + ')';
      });

    // --- cudaDeviceSynchronize ---
    code = code.replace(/(?<!__rt\.)\bcudaDeviceSynchronize\s*\(\s*\)/g, '__rt.cudaDeviceSynchronize()');

    // --- cudaGetDeviceCount ---
    code = code.replace(/cudaGetDeviceCount\s*\(\s*&?\s*([\w.\[\]]+)\s*\)/g, function(m, target) {
      return '(' + target.trim() + ' = __rt.getDeviceCount(), 0)';
    });

    // --- cudaSetDevice / cudaGetDevice ---
    code = code.replace(/cudaSetDevice\s*\(\s*([^)]+)\)/g, '__rt.setDevice($1)');
    code = code.replace(/cudaGetDevice\s*\(\s*&?\s*([\w.\[\]]+)\s*\)/g, function(m, target) {
      return '(' + target.trim() + ' = __rt.getDevice(), 0)';
    });

    // --- cudaDeviceCanAccessPeer / Enable / Disable ---
    code = code.replace(/cudaDeviceCanAccessPeer\s*\(\s*&?\s*([\w.\[\]]+)\s*,\s*([^,]+)\s*,\s*([^)]+)\)/g, function(m, target) {
      return '(' + target.trim() + ' = 1, 0)';
    });
    code = code.replace(/cudaDeviceEnablePeerAccess\s*\(\s*([^,)]+)(?:\s*,\s*[^)]+)?\)/g,
      '(__rt.enablePeerAccess ? __rt.enablePeerAccess($1) : 0)');
    code = code.replace(/cudaDeviceDisablePeerAccess\s*\([^)]*\)/g, '0');

    // --- cudaGetDeviceProperties ---
    code = code.replace(/cudaGetDeviceProperties\s*\(\s*&?\s*([\w.\[\]]+)\s*,\s*([^)]+)\)/g, function(m, target) {
      return '(' + target.trim() + ' = Object.assign({}, __rt.getProfile ? __rt.getProfile() : {}), 0)';
    });

    // --- cudaMemcpyPeer / cudaMemcpyPeerAsync ---
    code = code.replace(/cudaMemcpyPeer\s*\(\s*&?\s*([^,]+)\s*,\s*([^,]+)\s*,\s*&?\s*([^,]+)\s*,\s*([^,]+)\s*,\s*([^)]+)\)/g,
      '__rt.memcpyPeer($1, $2, $3, $4, $5)');
    code = code.replace(/cudaMemcpyPeerAsync\s*\(\s*&?\s*([^,]+)\s*,\s*([^,]+)\s*,\s*&?\s*([^,]+)\s*,\s*([^,]+)\s*,\s*([^,)]+)[^)]*\)/g,
      '__rt.memcpyPeer($1, $2, $3, $4, $5)');

    // --- NCCL Collectives & Setup ---
    code = code.replace(/ncclGetUniqueId\s*\(\s*&?\s*([\w.\[\]]+)\s*\)/g, function(m, target) {
      return '(' + target.trim() + ' = { id: 1 }, 0)';
    });
    code = code.replace(/ncclCommInitRank\s*\(\s*&?\s*([\w.\[\]]+)\s*,\s*([^,]+)\s*,\s*([^,]+)\s*,\s*([^)]+)\)/g,
      function(m, comm, nranks, id, rank) {
        return '(' + comm.trim() + ' = __rt.ncclCommInitRank(' + nranks.trim() + ', ' + rank.trim() + '), 0)';
      });
    code = code.replace(/ncclCommInitAll\s*\(\s*&?\s*([\w.\[\]]+)\s*,\s*([^,)]+)(?:,[^)]*)?\)/g,
      function(m, comms, nranks) {
        return '__rt.ncclCommInitAll(' + comms.trim() + ', ' + nranks.trim() + ')';
      });
    code = code.replace(/ncclAllReduce\s*\(\s*([^,]+),\s*([^,]+),\s*([^,]+),\s*([^,]+),\s*([^,]+),\s*([^,)]+)(?:,[^)]*)?\)/g,
      function(m, send, recv, count, dtype, op, comm) {
        return '__rt.ncclAllReduce(' + send.trim() + ', ' + recv.trim() + ', ' + count.trim() + ', ' + dtype.trim() + ', ' + op.trim() + ', ' + comm.trim() + ')';
      });
    code = code.replace(/ncclBroadcast\s*\(\s*([^,]+),\s*([^,]+),\s*([^,]+),\s*([^,]+),\s*([^,]+),\s*([^,)]+)(?:,[^)]*)?\)/g,
      function(m, send, recv, count, dtype, root, comm) {
        return '__rt.ncclBroadcast(' + send.trim() + ', ' + recv.trim() + ', ' + count.trim() + ', ' + dtype.trim() + ', ' + root.trim() + ', ' + comm.trim() + ')';
      });
    code = code.replace(/ncclReduceScatter\s*\(\s*([^,]+),\s*([^,]+),\s*([^,]+),\s*([^,]+),\s*([^,]+),\s*([^,)]+)(?:,[^)]*)?\)/g,
      function(m, send, recv, recvcount, dtype, op, comm) {
        return '__rt.ncclReduceScatter(' + send.trim() + ', ' + recv.trim() + ', ' + recvcount.trim() + ', ' + dtype.trim() + ', ' + op.trim() + ', ' + comm.trim() + ')';
      });
    code = code.replace(/ncclAllGather\s*\(\s*([^,]+),\s*([^,]+),\s*([^,]+),\s*([^,]+),\s*([^,)]+)(?:,[^)]*)?\)/g,
      function(m, send, recv, sendcount, dtype, comm) {
        return '__rt.ncclAllGather(' + send.trim() + ', ' + recv.trim() + ', ' + sendcount.trim() + ', ' + dtype.trim() + ', ' + comm.trim() + ')';
      });
    code = code.replace(/ncclCommDestroy\s*\([^)]*\)/g, '/* comm destroyed */ 0');

    // --- cudaMemcpyAsync — treat as sync ---
    code = code.replace(/cudaMemcpyAsync\s*\(\s*([^,]+),\s*([^,]+),\s*([^,]+),\s*cudaMemcpyHostToDevice[^)]*\)/g,
      function(m, dst, src, size) {
        return '__rt.cudaMemcpy(' + dst.trim() + ', ' + src.trim() + ', ' + size.trim() + ", 'H2D')";
      });
    code = code.replace(/cudaMemcpyAsync\s*\(\s*([^,]+),\s*([^,]+),\s*([^,]+),\s*cudaMemcpyDeviceToHost[^)]*\)/g,
      function(m, dst, src, size) {
        return '__rt.cudaMemcpy(' + dst.trim() + ', ' + src.trim() + ', ' + size.trim() + ", 'D2H')";
      });

    // --- Strip remaining unary address-of '&' before identifiers/expressions ---
    code = code.replace(/(?<=[([,{=?:;!]|\breturn\s+|\bcase\s+|^)\s*&(?![&=])\s*/gm, '');

    // --- cudaStreamCreate / cudaStreamSynchronize / cudaStreamDestroy — stub ---
    code = code.replace(/cudaStreamCreate\s*\(\s*&(\w+)\s*\)/g, '$1 = 0 /* stream stub */');
    code = code.replace(/cudaStreamSynchronize\s*\([^)]*\)/g, '__rt.cudaDeviceSynchronize()');
    code = code.replace(/cudaStreamDestroy\s*\([^)]*\)/g, '/* stream destroyed */');

    // --- cudaEventCreate / cudaEventRecord / cudaEventSynchronize / etc — stub ---
    code = code.replace(/cudaEventCreate\s*\(\s*&(\w+)\s*\)/g, '$1 = 0 /* event stub */');
    code = code.replace(/cudaEvent\w+\s*\([^)]*\)/g, '/* cuda event stub */');

    // --- dim3 ---
    // Use findMatchingDelimiter to handle nested expressions like dim3 sBlocks((N + 15) / 16, (N + 15) / 16);
    const dim3Pattern = /\bdim3\s+(\w+)\s*\(/g;
    let dMatch;
    while ((dMatch = dim3Pattern.exec(code)) !== null) {
      const pStart = dMatch.index + dMatch[0].length - 1;
      const pEnd = findMatchingDelimiter(code, pStart, '(', ')');
      if (pEnd === -1) continue;
      const name = dMatch[1];
      const args = code.substring(pStart + 1, pEnd);
      const parts = splitTopLevelCommas(args).map(function(a) { return a.trim(); });
      const x = parts[0] ? 'Math.floor(' + parts[0] + ')' : '1';
      const y = parts[1] ? 'Math.floor(' + parts[1] + ')' : '1';
      const z = parts[2] ? 'Math.floor(' + parts[2] + ')' : '1';
      const repl = 'let ' + name + ' = {x: ' + x + ', y: ' + y + ', z: ' + z + '}';
      code = code.substring(0, dMatch.index) + repl + code.substring(pEnd + 1);
      dim3Pattern.lastIndex = dMatch.index + repl.length;
    }

    // --- printf & stream output (std::cout / cout) ---
    code = transformPrintf(code);
    code = transformCout(code);
    code = code.replace(/\busing\s+namespace\s+std\s*;/g, '');
    code = code.replace(/\busing\s+std\s*::\s*\w+\s*;/g, '');
    code = code.replace(/\bstd\s*::\s*endl\b/g, '"\\n"');
    code = code.replace(/\bendl\b/g, '"\\n"');

    // --- new type[N] allocations ---
    code = code.replace(/new\s+float\s*\[\s*([^\]]+)\s*\]/g, 'new Float32Array($1)');
    code = code.replace(/new\s+double\s*\[\s*([^\]]+)\s*\]/g, 'new Float64Array($1)');
    code = code.replace(/new\s+int\s*\[\s*([^\]]+)\s*\]/g, 'new Int32Array($1)');
    code = code.replace(/new\s+unsigned\s+int\s*\[\s*([^\]]+)\s*\]/g, 'new Uint32Array($1)');
    code = code.replace(/new\s+char\s*\[\s*([^\]]+)\s*\]/g, 'new Uint8Array($1)');
    code = code.replace(/new\s+unsigned\s+char\s*\[\s*([^\]]+)\s*\]/g, 'new Uint8Array($1)');

    // --- delete[] ---
    code = code.replace(/delete\s*\[\s*\]\s*\w+\s*;/g, '/* freed */;');

    // --- malloc / free ---
    code = code.replace(/\bmalloc\s*\(\s*([^)]+)\)/g, 'new ArrayBuffer($1)');
    code = code.replace(/\bfree\s*\(\s*\w+\s*\)/g, '/* freed */');

    // --- Type declarations ---
    code = transformTypeDeclarations(code);

    // Ceil divisions in host code: (N + TILE - 1) / TILE → Math.floor((N + TILE - 1) / TILE)
    code = code.replace(/\b(\w+)\s*\/=\s*(\d+)\b/g, '$1 = Math.floor($1 / $2)');
    code = code.replace(/\(([a-zA-Z0-9_.]+\s*[+\-*]\s*[a-zA-Z0-9_.]+)\)\s*\/\s*([a-zA-Z0-9_]+)\b/g, 'Math.floor(($1) / $2)');

    // --- Math functions ---
    code = transformMathFunctions(code);

    // --- Constants ---
    code = transformConstants(code);

    // --- Float literal suffixes ---
    code = code.replace(/(\d+\.?\d*)[fF]\b/g, '$1');
    code = code.replace(/(\d*\.\d+)[fF]\b/g, '$1');

    // --- Type casts ---
    code = transformTypeCasts(code);

    // --- Strip remaining C++ qualifiers ---
    code = code.replace(/\bextern\s+"C"\s*\{/g, '{');
    code = code.replace(/\bextern\s+"C"/g, '');
    code = code.replace(/\bstatic\b\s*/g, '');
    code = code.replace(/\binline\b\s*/g, '');
    code = code.replace(/\bvolatile\b\s*/g, '');
    code = code.replace(/\b__host__\b\s*/g, '');
    code = code.replace(/\b__forceinline__\b\s*/g, '');
    code = code.replace(/\b__restrict__\b\s*/g, '');
    code = code.replace(/\brestrict\b\s*/g, '');

    // --- cudaMemcpyPeer & Peer Access ---
    code = code.replace(/cudaMemcpyPeer\s*\(/g, '__rt.memcpyPeer(');
    code = code.replace(/cudaDeviceEnablePeerAccess\s*\(/g, '__rt.cudaDeviceEnablePeerAccess(');
    code = code.replace(/cudaDeviceDisablePeerAccess\s*\(/g, '__rt.cudaDeviceDisablePeerAccess(');

    // --- cudaGetLastError / cudaPeekAtLastError ---
    code = code.replace(/cudaGetLastError\s*\(\s*\)/g, '__rt.cudaGetLastError()');
    code = code.replace(/cudaPeekAtLastError\s*\(\s*\)/g, '__rt.cudaPeekAtLastError()');
    code = code.replace(/cudaGetErrorString\s*\(([^)]*)\)/g, '__rt.cudaGetErrorString($1)');

    return code;
  }

  /**
   * Transform kernel<<<grid, block[, shmem]>>>(args) launch syntax.
   */
  function transformKernelLaunches(code, kernelNames, warnings) {
    // Only match known extracted kernel names to avoid false matches on "i < N"
    const namesPattern = (kernelNames && kernelNames.length > 0)
      ? kernelNames.map(function(n) { return n.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }).join('|')
      : '[a-zA-Z_]\\w*';
    const launchPattern = new RegExp('\\b(' + namesPattern + ')\\s*(?:<[a-zA-Z0-9_,\\s*]+>)?\\s*<<<', 'g');
    let m;

    while ((m = launchPattern.exec(code)) !== null) {
      const kernelName = m[1];
      const tripleStart = code.indexOf('<<<', m.index);

      // Find the matching >>>
      let tripleEnd = -1;
      let depth = 0;
      for (let i = tripleStart; i < code.length - 2; i++) {
        if (code[i] === '<' && code[i + 1] === '<' && code[i + 2] === '<') {
          depth++;
          i += 2;
        } else if (code[i] === '>' && code[i + 1] === '>' && code[i + 2] === '>') {
          depth--;
          if (depth === 0) {
            tripleEnd = i + 3;
            break;
          }
          i += 2;
        }
      }

      if (tripleEnd === -1) {
        warnings.push('Could not find matching >>> for kernel launch: ' + kernelName);
        continue;
      }

      const configStr = code.substring(tripleStart + 3, tripleEnd - 3).trim();
      const configParts = splitTopLevelCommas(configStr);

      let grid = configParts[0] ? configParts[0].trim() : '{x:1,y:1,z:1}';
      let block = configParts[1] ? configParts[1].trim() : '{x:1,y:1,z:1}';
      let shmem = configParts[2] ? configParts[2].trim() : '0';
      // configParts[3] would be stream — ignore

      // If grid/block are plain numbers, wrap as dim3
      if (/^\d+$/.test(grid)) grid = '{x:' + grid + ', y:1, z:1}';
      if (/^\d+$/.test(block)) block = '{x:' + block + ', y:1, z:1}';

      // Find the argument list that follows >>>
      const afterTriple = code.substring(tripleEnd).trimStart();
      const parenIdx = code.indexOf('(', tripleEnd);
      if (parenIdx === -1) continue;

      const parenEnd = findMatchingDelimiter(code, parenIdx, '(', ')');
      if (parenEnd === -1) continue;

      const argsStr = code.substring(parenIdx + 1, parenEnd).trim();

      // Build the __rt.launch call
      let launchArgs = '__kernel_' + kernelName + ', ' + grid + ', ' + block + ', ' + shmem;
      if (argsStr.length > 0) {
        launchArgs += ', ' + argsStr;
      }
      const replacement = '__rt.launch(' + launchArgs + ')';

      code = code.substring(0, m.index) + replacement + code.substring(parenEnd + 1);
      launchPattern.lastIndex = m.index + replacement.length;
    }

    return code;
  }

  /**
   * Transform C printf format strings to JavaScript string concatenation.
   * Handles: %d, %i, %u, %f, %lf, %e, %g, %s, %ld, %lu, %lld, %llu, %x, %p, %%
   */
  function transformPrintf(code) {
    const pattern = /\bprintf\s*\(/g;
    let m;

    while ((m = pattern.exec(code)) !== null) {
      const parenStart = m.index + m[0].length - 1;
      const parenEnd = findMatchingDelimiter(code, parenStart, '(', ')');
      if (parenEnd === -1) continue;

      const inner = code.substring(parenStart + 1, parenEnd);
      const args = splitTopLevelCommas(inner);

      if (args.length === 0) continue;

      let formatStr = args[0].trim();
      const printArgs = args.slice(1).map(function(a) { return a.trim(); });

      // Check if format string is a string literal
      if (/^\x00STR\d+\x00$/.test(formatStr) || /^".*"$/.test(formatStr)) {
        // It's a protected string or a direct string — we'll build concatenation
        // For simplicity, pass format + args to __rt.printf which handles C-style formatting
        const replacement = '__rt.printf(' + args.join(', ') + ')';
        code = code.substring(0, m.index) + replacement + code.substring(parenEnd + 1);
        pattern.lastIndex = m.index + replacement.length;
      } else {
        // Not a string literal — might be a variable
        const replacement = '__rt.printf(' + args.join(', ') + ')';
        code = code.substring(0, m.index) + replacement + code.substring(parenEnd + 1);
        pattern.lastIndex = m.index + replacement.length;
      }
    }

    return code;
  }

  /**
   * Split stream insertion '<<' chains outside strings and parens.
   */
  function splitStreamShift(str) {
    const parts = [];
    let depth = 0;
    let inString = false;
    let strChar = '';
    let current = '';

    for (let i = 0; i < str.length; i++) {
      const ch = str[i];
      if (inString) {
        if (ch === '\\') { current += ch + (str[++i] || ''); continue; }
        if (ch === strChar) inString = false;
        current += ch;
        continue;
      }
      if (ch === '"' || ch === "'") {
        inString = true;
        strChar = ch;
        current += ch;
        continue;
      }
      if (ch === '(' || ch === '[' || ch === '{') depth++;
      else if (ch === ')' || ch === ']' || ch === '}') depth--;

      if (depth === 0 && ch === '<' && str[i + 1] === '<') {
        parts.push(current.trim());
        current = '';
        i++;
        continue;
      }
      current += ch;
    }
    if (current.trim().length > 0) parts.push(current.trim());
    return parts;
  }

  /**
   * Transform std::cout << a << b << std::endl; to __rt.printf(...)
   */
  function transformCout(code) {
    const pattern = /\b(?:std\s*::\s*)?(?:cout|cerr)\s*<<\s*/g;
    let m;
    while ((m = pattern.exec(code)) !== null) {
      let semiIdx = -1;
      let inString = false;
      let strChar = '';
      for (let j = m.index; j < code.length; j++) {
        const ch = code[j];
        if (inString) {
          if (ch === '\\') { j++; continue; }
          if (ch === strChar) inString = false;
          continue;
        }
        if (ch === '"' || ch === "'") {
          inString = true;
          strChar = ch;
          continue;
        }
        if (ch === ';') {
          semiIdx = j;
          break;
        }
      }
      if (semiIdx === -1) continue;

      const chainStr = code.substring(m.index + m[0].length, semiIdx);
      const parts = splitStreamShift(chainStr);

      const jsParts = [];
      for (let k = 0; k < parts.length; k++) {
        let p = parts[k].trim();
        // Ignore <iomanip> manipulators
        if (/^(?:std\s*::\s*)?(?:fixed|scientific|hex|dec|left|right|boolalpha|noboolalpha|showpoint|noshowpoint|setprecision\s*\(.*?\)|setw\s*\(.*?\)|setfill\s*\(.*?\))$/.test(p)) {
          continue;
        }
        if (p === 'std::endl' || p === 'endl') jsParts.push('"\\n"');
        else if (p === "'\\n'") jsParts.push('"\\n"');
        else jsParts.push(p);
      }

      if (jsParts.length === 0) {
        code = code.substring(0, m.index) + '/* iomanip */' + code.substring(semiIdx);
        pattern.lastIndex = m.index + '/* iomanip */'.length;
        continue;
      }

      const replacement = '__rt.printf(' + jsParts.join(' + ') + ')';
      code = code.substring(0, m.index) + replacement + code.substring(semiIdx);
      pattern.lastIndex = m.index + replacement.length;
    }
    return code;
  }

  // ---------------------------------------------------------------------------
  // Vector type helpers
  // ---------------------------------------------------------------------------

  function transformVectorTypes(code) {
    // make_float4(a,b,c,d) → {x:a, y:b, z:c, w:d}
    code = code.replace(/make_float4\s*\(\s*([^,]+),\s*([^,]+),\s*([^,]+),\s*([^)]+)\)/g,
      '{x:$1, y:$2, z:$3, w:$4}');
    code = code.replace(/make_float3\s*\(\s*([^,]+),\s*([^,]+),\s*([^)]+)\)/g,
      '{x:$1, y:$2, z:$3}');
    code = code.replace(/make_float2\s*\(\s*([^,]+),\s*([^)]+)\)/g,
      '{x:$1, y:$2}');
    code = code.replace(/make_int4\s*\(\s*([^,]+),\s*([^,]+),\s*([^,]+),\s*([^)]+)\)/g,
      '{x:$1, y:$2, z:$3, w:$4}');
    code = code.replace(/make_int3\s*\(\s*([^,]+),\s*([^,]+),\s*([^)]+)\)/g,
      '{x:$1, y:$2, z:$3}');
    code = code.replace(/make_int2\s*\(\s*([^,]+),\s*([^)]+)\)/g,
      '{x:$1, y:$2}');
    code = code.replace(/make_double2\s*\(\s*([^,]+),\s*([^)]+)\)/g,
      '{x:$1, y:$2}');
    code = code.replace(/make_uint2\s*\(\s*([^,]+),\s*([^)]+)\)/g,
      '{x:$1, y:$2}');

    return code;
  }

  // ---------------------------------------------------------------------------
  // Pass 5: Final syntax cleanup
  // ---------------------------------------------------------------------------

  function finalCleanup(code) {
    // Fix char literals containing newlines or escaped newlines
    code = code.replace(/'\n'/g, '"\\n"');
    code = code.replace(/'\r\n'/g, '"\\n"');
    code = code.replace(/'\\n'/g, '"\\n"');
    code = code.replace(/'\\t'/g, '"\\t"');
    code = code.replace(/'\\0'/g, '0');

    // Remove empty statements (multiple semicolons)
    code = code.replace(/;(\s*;)+/g, ';');

    // Remove lines that are only whitespace
    code = code.replace(/^\s*$/gm, '');

    // Collapse multiple blank lines into one
    code = code.replace(/\n{3,}/g, '\n\n');

    // Strip leading/trailing whitespace
    code = code.trim();

    return code;
  }

  // ---------------------------------------------------------------------------
  // Device function transformation
  // ---------------------------------------------------------------------------

  /**
   * Transform a __device__ function similarly to a kernel, but without
   * the runtime parameter prefix (device functions are called from kernels
   * which already have access to those variables via closure or pass-through).
   * We emit them as regular JS functions prefixed with __device_.
   */
  function transformDeviceFunction(func, allDeviceNames) {
    let body = func.body;

    // Apply kernel-like transforms to the body
    const ptrParams = new Set();
    for (let i = 0; i < func.params.length; i++) {
      if (func.params[i].isPointer) ptrParams.add(func.params[i].name);
    }

    body = body.replace(/\bthreadIdx\s*\.\s*([xyz])/g, '__tid.$1');
    body = body.replace(/\bblockIdx\s*\.\s*([xyz])/g, '__bid.$1');
    body = body.replace(/\bblockDim\s*\.\s*([xyz])/g, '__bdim.$1');
    body = body.replace(/\bgridDim\s*\.\s*([xyz])/g, '__gdim.$1');
    body = body.replace(/__syncthreads\s*\(\s*\)/g, '__sync()');
    body = body.replace(/\bprintf\s*\(/g, '__printf(');

    body = transformPointerAccess(body, ptrParams);
    body = transformTypeDeclarations(body);
    body = transformMathFunctions(body);
    body = transformConstants(body);
    body = transformTypeCasts(body);
    body = transformVectorTypes(body);
    body = body.replace(/(\d+\.?\d*)[fF]\b/g, '$1');
    body = body.replace(/(\d*\.\d+)[fF]\b/g, '$1');

    // Build parameter list (just names)
    const paramNames = func.params.map(function(p) { return p.name; }).join(', ');

    // Determine return type (we stripped it, but device functions might return values)
    return 'function __device_' + func.name + '(' + paramNames + ') {\n' + body + '\n  }';
  }

  // ---------------------------------------------------------------------------
  // Main transpile function
  // ---------------------------------------------------------------------------

  /**
   * Transpile CUDA C++ source code to JavaScript.
   * @param {string} cudaSource  The raw CUDA C++ source code.
   * @returns {{ success: boolean, code: string, errors: string[], kernelNames: string[], warnings: string[] }}
   */

  // ---- Instrumentation: branch outcomes and static FLOP estimates ----
  function findClose(src, openIdx) {
    let d = 0;
    for (let i = openIdx; i < src.length; i++) {
      const c = src[i];
      if (c === '(') d++;
      else if (c === ')') { d--; if (d === 0) return i; }
    }
    return -1;
  }

  /** if (c) -> if (__atomic.br(site, (c))): lets the runtime see per-lane outcomes. */
  function instrumentBranches(body) {
    let out = '', i = 0, site = 0;
    const re = /\bif\s*\(/g;
    let m;
    while ((m = re.exec(body)) !== null) {
      const open = m.index + m[0].length - 1;
      const close = findClose(body, open);
      if (close < 0) break;
      out += body.slice(i, open + 1) + '__atomic.br(' + (site++) + ', (' + body.slice(open + 1, close) + '))';
      i = close;
      re.lastIndex = close;
    }
    return out + body.slice(i);
  }

  /** Statically estimate FLOPs for one simple statement (float evidence required). */
  function estimateStatementFlops(stmt) {
    if (/yield|__tid|__bid|__bdim|__gdim|__atomic|__shared/.test(stmt.replace(/__shared\.get2DArray[^;]*/, ''))) {
      if (/__atomic|yield/.test(stmt)) return 0;
    }
    let t = stmt;
    // strip index expressions: .get(...), .set(first-arg, ...), [..]
    t = t.replace(/\.get\(([^()]|\([^()]*\))*\)/g, '.get()');
    t = t.replace(/\.set\(([^,()]|\([^()]*\))*,/g, '.set(');
    t = t.replace(/\[[^\[\]]*\]/g, '[]');
    const evidence = /\.get\(|\.set\(|\d\.\d|\bMath\.|\[\]|[+\-*\/]=/.test(t);
    if (!evidence) return 0;
    if (/__tid|__bid|__bdim|__gdim/.test(t)) return 0;
    let n = 0;
    n += (t.match(/Math\.(max|min|sqrt|exp|log|pow|abs|tanh|sin|cos|fround)/g) || []).length;
    t = t.replace(/\+\+|--/g, '');
    n += (t.match(/[+\-*\/]=|(?<![+\-*\/=<>!&|])[+\-*\/](?![+\-*\/=])/g) || []).length;
    return n;
  }

  /** Charge estimated FLOPs before each executed arithmetic statement. */
  function instrumentFlops(body) {
    let out = '', cur = '', depth = 0;
    const flush = (term) => {
      let stmt = cur, prefix = '';
      // peel control headers: for(...), while(...), if(...), else
      for (;;) {
        const hm = /^\s*(?:else\s+)?(?:(?:for|while|if)\s*\(|else\b)/.exec(stmt);
        if (!hm) break;
        if (/\($/.test(hm[0])) {
          const open = hm[0].length - 1, close = findClose(stmt, open);
          if (close < 0) break;
          prefix += stmt.slice(0, close + 1); stmt = stmt.slice(close + 1);
        } else { prefix += stmt.slice(0, hm[0].length); stmt = stmt.slice(hm[0].length); }
      }
      const n = term === ';' ? estimateStatementFlops(stmt) : 0;
      if (n > 0) {
        out += prefix.length ? prefix + '{__atomic.fl(' + n + ');' + stmt + ';}' : '__atomic.fl(' + n + ');' + stmt + ';';
      } else out += cur + (term || '');
      cur = '';
    };
    for (let i = 0; i < body.length; i++) {
      const c = body[i];
      if (c === '(') depth++;
      if (c === ')') depth--;
      if (depth === 0 && (c === ';' || c === '{' || c === '}')) {
        flush(c === ';' ? ';' : null);
        if (c !== ';') out += c;
      } else cur += c;
    }
    out += cur;
    return out;
  }



  // ---- Integer division: C++ truncates when both operands are integers; JS never does ----
  const INT_TYPE_RE = '(?:unsigned\\s+int|unsigned|size_t|int|long\\s+long|long|short|char|uint32_t|int32_t|uint64_t|int64_t|uint8_t)';

  function collectIntNames(body, params, macroInts) {
    const ints = new Set(macroInts);
    const floats = new Set();
    (params || []).forEach(function (p) {
      if (p.isPointer) return;
      if (new RegExp('^(?:const\\s+)?' + INT_TYPE_RE + '$').test(String(p.type).trim())) ints.add(p.name);
      else floats.add(p.name);
    });
    const decl = new RegExp('\\b(?:const\\s+)?(' + INT_TYPE_RE + '|float|double)\\s+([^;(){}]*?)(?=[;)])', 'g');
    let m;
    while ((m = decl.exec(body)) !== null) {
      const isInt = m[1] !== 'float' && m[1] !== 'double';
      let depth = 0, cur = '';
      const parts = [];
      for (const ch of m[2]) {
        if ('([{'.indexOf(ch) >= 0) depth++;
        else if (')]}'.indexOf(ch) >= 0) depth--;
        if (ch === ',' && depth === 0) { parts.push(cur); cur = ''; } else cur += ch;
      }
      parts.push(cur);
      parts.forEach(function (part) {
        const nm = /^\s*\**\s*(\w+)/.exec(part);
        if (nm && !/^\s*\*/.test(part)) { if (isInt) { ints.add(nm[1]); floats.delete(nm[1]); } else { floats.add(nm[1]); ints.delete(nm[1]); } }
      });
    }
    return ints;
  }

  function isIntExpr(expr, ints) {
    let e = expr.replace(/Math\.trunc\(/g, '(');
    if (/\(\s*(?:float|double)\s*\)/.test(e)) return false;
    if (/\.get\(|\[|\d\.\d|\d\.(?!\w)|(?<![\w])\.\d|\d[eE][+-]?\d|\b\d+\.?\d*[fF]\b/.test(e)) return false;
    e = e.replace(/\(\s*(?:unsigned\s+int|unsigned|size_t|int|long\s+long|long|short|uint32_t|int32_t|uint64_t|int64_t)\s*\)/g, ' ');
    if (/[A-Za-z_]\w*\s*\(/.test(e)) return false; // a function call: type unknown
    const ids = e.match(/(?<![.\w])[A-Za-z_]\w*/g) || [];
    const builtins = { blockDim: 1, gridDim: 1, threadIdx: 1, blockIdx: 1, __bdim: 1, __gdim: 1, __tid: 1, __bid: 1, warpSize: 1 };
    return ids.every(function (id) { return ints.has(id) || builtins[id]; });
  }

  function atomBackward(src, end) {
    // returns start index of the atom that ends right before `end`, or -1
    let i = end - 1;
    while (i >= 0 && /\s/.test(src[i])) i--;
    if (i < 0) return -1;
    if (src[i] === ')' || src[i] === ']') {
      const open = src[i] === ')' ? '(' : '[', close = src[i];
      let d = 0;
      for (; i >= 0; i--) {
        if (src[i] === close) d++;
        else if (src[i] === open) { d--; if (d === 0) break; }
      }
      if (i < 0) return -1;
      i--;
      while (i >= 0 && /[\w.$]/.test(src[i])) i--;
      return i + 1;
    }
    const j = i;
    while (i >= 0 && /[\w.$]/.test(src[i])) i--;
    return i === j ? -1 : i + 1;
  }

  function atomForward(src, start) {
    let i = start;
    while (i < src.length && /\s/.test(src[i])) i++;
    if (src[i] === '-' || src[i] === '+') i++;
    while (i < src.length && /\s/.test(src[i])) i++;
    for (;;) {
      if (src[i] === '(') {
        let d = 0;
        for (; i < src.length; i++) {
          if (src[i] === '(') d++;
          else if (src[i] === ')') { d--; if (d === 0) { i++; break; } }
        }
        // a cast "(int)" is followed by its operand
        if (/^\(\s*(?:unsigned\s+int|unsigned|size_t|int|long|short|float|double|uint32_t)\s*\)$/.test(src.slice(start, i).trim()) && i < src.length) {
          const next = atomForward(src, i);
          return next;
        }
        return i;
      }
      const s0 = i;
      while (i < src.length && /[\w.$]/.test(src[i])) i++;
      if (i === s0) return -1;
      while (src[i] === '(' || src[i] === '[') {
        const open = src[i], close = open === '(' ? ')' : ']';
        let d = 0;
        for (; i < src.length; i++) {
          if (src[i] === open) d++;
          else if (src[i] === close) { d--; if (d === 0) { i++; break; } }
        }
      }
      return i;
    }
  }

  /** Wraps `a / b` in Math.trunc(...) when every identifier in the whole multiplicative term is an integer. */
  function fixIntDivision(body, params, macroInts) {
    const ints = collectIntNames(body, params, macroInts);
    let src = body;
    let pos = 0;
    while ((pos = src.indexOf('/', pos)) !== -1) {
      const prev = src[pos - 1], next = src[pos + 1];
      if (next === '/' || next === '*' || next === '=' || prev === '/' || prev === '*') { pos++; continue; }
      // left multiplicative chain
      let start = pos;
      for (;;) {
        const a = atomBackward(src, start);
        if (a < 0) break;
        start = a;
        let k = a - 1;
        while (k >= 0 && /\s/.test(src[k])) k--;
        if (k >= 0 && (src[k] === '*' || src[k] === '/' || src[k] === '%') && src[k - 1] !== src[k]) start = k; else break;
      }
      const rEnd = atomForward(src, pos + 1);
      if (rEnd < 0 || start >= pos) { pos++; continue; }
      if (/\(\s*(?:float|double)\s*\)\s*$/.test(src.slice(0, start))) { pos++; continue; }
      const left = src.slice(start, pos), right = src.slice(pos + 1, rEnd);
      if (isIntExpr(left, ints) && isIntExpr(right, ints)) {
        const wrapped = 'Math.trunc(' + left + '/' + right + ')';
        src = src.slice(0, start) + wrapped + src.slice(rEnd);
        pos = start + wrapped.length;
      } else pos++;
    }
    return src;
  }

  // ---- Source normalization: C++ spellings Gpubox's string transpiler does not know ----
  function normalizeCuda(src) {
    // integer literal suffixes: 5u, 0xffffffffu, 1ull ...
    src = src.replace(/(?<![\w.])(0[xX][0-9a-fA-F]+|\d+)(?:[uU][lL]{0,2}|[lL]{1,2}[uU]?)\b/g, '$1');
    src = src.replace(/\bconstexpr\b/g, 'const');
    src = src.replace(/(__shared__\s+)(?:const\s+)?(?:unsigned\s+int|unsigned|uint32_t|uint64_t|size_t|long\s+long|long)\s+(\w+\s*\[)/g, '$1int $2');
    src = src.replace(/\bunsigned\b(?!\s+(?:int|char|short|long)\b)/g, 'unsigned int');
    src = src.replace(/\b__(?:noinline|forceinline|inline)__\b\s*/g, '');
    src = src.replace(/\bCUDART_INF_F\b/g, 'INFINITY').replace(/\bCUDART_NAN_F\b/g, 'NAN');
    // float4 through reinterpret_cast: one 16-byte access per use
    // reinterpret_cast<float4*>(P)[v] and reinterpret_cast<float4*>(P + off)[v]
    const castPtr = '\\breinterpret_cast\\s*<\\s*(?:const\\s+)?float4\\s*\\*\\s*>\\s*\\(\\s*(\\w+)\\s*(?:\\+\\s*((?:[^()\\[\\]]|\\([^()]*\\))+?))?\\s*\\)\\s*\\[([^\\]]+)\\]';
    src = src.replace(new RegExp(castPtr + '\\s*=(?!=)\\s*([^;]+);', 'g'), function (m, p, off, idx, val) { return p + '.setVec4(' + idx + ', ' + val.trim() + (off ? ', ' + off.trim() : '') + ');'; });
    src = src.replace(new RegExp(castPtr, 'g'), function (m, p, off, idx) { return p + '.getVec4(' + idx + (off ? ', ' + off.trim() : '') + ')'; });
    src = src.replace(/\b(?:const\s+)?float4\s+(\w+)\s*;/g, 'let $1 = {x:0,y:0,z:0,w:0};');
    src = src.replace(/\b(?:const\s+)?float4\s+(\w+)\s*=/g, 'let $1 =');
    src = src.replace(/\bmake_float4\s*\(([^(),]+),([^(),]+),([^(),]+),([^(),]+)\)/g, '{x:$1,y:$2,z:$3,w:$4}');
    return src;
  }

  const ERF_HELPER = 'function __erf(x){var t=1/(1+0.3275911*Math.abs(x));var y=1-(((((1.061405429*t-1.453152027)*t)+1.421413741)*t-0.284496736)*t+0.254829592)*t*Math.exp(-x*x);return x>=0?y:-y;}\n';

  function transpile(cudaSource) {
    const errors = [];
    const warnings = [];
    const kernelNames = [];

    if (!cudaSource || typeof cudaSource !== 'string' || cudaSource.trim().length === 0) {
      return { success: false, code: '', errors: ['Empty source'], kernelNames: [], warnings: [] };
    }

    try {
      let src = cudaSource;

      // Strip extern "C" linkage before string protection
      src = src.replace(/\bextern\s+"C"\s*\{/g, '{');
      src = src.replace(/\bextern\s+"C"\s*/g, '');
      src = normalizeCuda(src);
      src = src.replace(/\bextern\b\s*/g, '');

      // --- Protect strings and comments ---
      const prot = protectStringsAndComments(src);
      src = prot.text;

      // --- Pass 1: Preprocessor ---
      const prep = preprocessorPass(src, warnings);
      src = prep.src;
      const globalMacros = prep.globalMacros;
      const macroInts = prep.globalMacros.map(function (m) { return /^const (\w+) = -?[\d\s+\-*()]+;$/.exec(m); }).filter(Boolean).map(function (m) { return m[1]; });

      // --- Vector types (before kernel extraction since they appear in params) ---
      src = transformVectorTypes(src);

      // --- Pass 2: Extract kernels ---
      const extracted = extractKernels(src);
      const hostSrc = extracted.remaining;

      // --- Check for explicitly unsupported CUDA features ---
      if (/\b(?:__)?asm(?:__)?\s*(?:volatile)?\s*\(/i.test(src) || /\b(?:__)?asm(?:__)?\s*\{/i.test(src)) {
        errors.push('Unsupported CUDA feature: Inline PTX assembly (__asm__) is not supported in browser-based simulator');
      }

      if (/\bcudaGraph(?:Create|Launch|Destroy|AddKernelNode|ExecUpdate)\b/.test(src)) {
        errors.push('Unsupported CUDA feature: CUDA Graph API (cudaGraph*) is not supported in client-side simulator');
      }

      if (/\b(?:nvcuda::)?wmma\b/.test(src)) {
        errors.push('Unsupported CUDA feature: Tensor Core WMMA API (nvcuda::wmma) is not supported in client-side simulator');
      }

      for (let i = 0; i < extracted.kernels.length; i++) {
        if (/<<<[\s\S]*?>>>/.test(extracted.kernels[i].body)) {
          errors.push('Unsupported CUDA feature: Dynamic Parallelism (nested kernel launch <<<...>>>) inside kernel "' + extracted.kernels[i].name + '" is not supported in client-side simulator');
        }
      }
      for (let i = 0; i < extracted.deviceFuncs.length; i++) {
        if (/<<<[\s\S]*?>>>/.test(extracted.deviceFuncs[i].body)) {
          errors.push('Unsupported CUDA feature: Dynamic Parallelism (nested kernel launch <<<...>>>) inside device function "' + extracted.deviceFuncs[i].name + '" is not supported in client-side simulator');
        }
      }

      if (errors.length > 0) {
        return {
          success: false,
          code: '',
          errors: errors,
          kernelNames: [],
          warnings: warnings
        };
      }

      // Collect device function names for cross-referencing
      const deviceNames = extracted.deviceFuncs.map(function(f) { return f.name; });

      // --- Transform device functions ---
      const deviceFuncCode = [];
      for (let i = 0; i < extracted.deviceFuncs.length; i++) {
        const func = extracted.deviceFuncs[i];
        const code = transformDeviceFunction(func, deviceNames);
        deviceFuncCode.push('  ' + prot.restore(code));
      }

      // --- Transform kernels ---
      const kernelCode = [];
      for (let i = 0; i < extracted.kernels.length; i++) {
        const kernel = extracted.kernels[i];
        kernelNames.push(kernel.name);

        // Transform the kernel body
        const transformedBody = instrumentFlops(instrumentBranches(transformKernelBody(fixIntDivision(kernel.body, kernel.params, macroInts), kernel.params, deviceNames)));

        // Build the JS function
        const paramNames = kernel.params.map(function(p) { return p.name; }).join(', ');
        const runtimeParams = '__tid, __bid, __bdim, __gdim, __shared, __sync, __atomic, __printf';
        const allParams = runtimeParams + (paramNames.length > 0 ? ', ' + paramNames : '');

        let funcCode = '  // Kernel: ' + kernel.name + '\n';
        funcCode += '  function* __kernel_' + kernel.name + '(' + allParams + ') {\n';
        funcCode += '    ' + prot.restore(transformedBody).trim().split('\n').join('\n    ') + '\n';
        funcCode += '  }';
        kernelCode.push(funcCode);
      }

      // --- Pass 3: Transform host code ---
      let hostCode = transformHostCode(hostSrc, kernelNames, warnings);

      // --- Restore strings and comments ---
      hostCode = prot.restore(hostCode);

      // --- Pass 5: Final cleanup ---
      hostCode = finalCleanup(hostCode);

      // --- Assemble output ---
      let output = '// Transpiled from CUDA source\n';
      output += '\n' + ERF_HELPER;

      // Global constants & macros (#define)
      if (globalMacros.length > 0) {
        output += '\n// Preprocessor Definitions\n';
        output += globalMacros.join('\n') + '\n';
      }

      // Device functions first (kernels may call them)
      if (deviceFuncCode.length > 0) {
        output += '\n// Device functions\n';
        output += deviceFuncCode.join('\n\n') + '\n';
      }

      // Kernels
      if (kernelCode.length > 0) {
        output += '\n' + kernelCode.join('\n\n') + '\n';
      }

      // Host code
      output += '\n// Host code\n';
      output += hostCode + '\n';

      return {
        success: true,
        code: output,
        errors: errors,
        kernelNames: kernelNames,
        warnings: warnings,
      };

    } catch (e) {
      errors.push('Transpilation error: ' + (e.message || String(e)));
      return {
        success: false,
        code: '',
        errors: errors,
        kernelNames: kernelNames,
        warnings: warnings,
      };
    }
  }

  // ---------------------------------------------------------------------------
  // Quick transpile: returns just the code string or throws
  // ---------------------------------------------------------------------------

  function quickTranspile(cudaSource) {
    const result = transpile(cudaSource);
    if (!result.success) {
      throw new Error('Transpilation failed: ' + result.errors.join('; '));
    }
    return result.code;
  }

  // ---------------------------------------------------------------------------
  // Validate: check transpiled output for obvious issues
  // ---------------------------------------------------------------------------

  function validate(transpiledCode) {
    const issues = [];

    // Check for remaining CUDA-isms that should have been transformed
    if (/\bcudaMalloc\b/.test(transpiledCode)) issues.push('Untranspiled cudaMalloc');
    if (/\bcudaFree\b/.test(transpiledCode)) issues.push('Untranspiled cudaFree');
    if (/\bcudaMemcpy\b/.test(transpiledCode)) issues.push('Untranspiled cudaMemcpy');
    if (/<<</.test(transpiledCode)) issues.push('Untranspiled kernel launch <<<>>>');
    if (/\bthreadIdx\b/.test(transpiledCode)) issues.push('Untranspiled threadIdx');
    if (/\bblockIdx\b/.test(transpiledCode)) issues.push('Untranspiled blockIdx');
    if (/\b__global__\b/.test(transpiledCode)) issues.push('Untranspiled __global__');
    if (/\b__device__\b/.test(transpiledCode)) issues.push('Untranspiled __device__');
    if (/\b__shared__\b/.test(transpiledCode)) issues.push('Untranspiled __shared__');
    if (/\bfloat\s+\w/.test(transpiledCode)) issues.push('Possible untranspiled float declaration');
    if (/#include\b/.test(transpiledCode)) issues.push('Untranspiled #include');

    // Try to parse as JS
    try {
      new Function('__rt', transpiledCode);
    } catch (e) {
      issues.push('JS parse error: ' + e.message);
    }

    return issues;
  }

  // ---------------------------------------------------------------------------
  // Export
  // ---------------------------------------------------------------------------

  var CudaTranspiler = {
    /** Full transpile with metadata */
    transpile: transpile,

    /** Quick transpile — returns code string or throws */
    quickTranspile: quickTranspile,

    /** Validate transpiled output */
    validate: validate,

    /** Version */
    version: '1.0.0',
  };

  // Export for browser
  // globalThis works on the main thread and inside Web Workers (no `window`)
  if (typeof globalThis !== 'undefined') {
    globalThis.CudaTranspiler = CudaTranspiler;
  }

  // Export for Node.js / CommonJS
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = CudaTranspiler;
  }

})();
