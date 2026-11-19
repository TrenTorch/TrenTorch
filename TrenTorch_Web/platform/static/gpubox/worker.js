// Classic Web Worker that runs learner CUDA kernels on the Gpubox simulator.
// Served from /gpubox/ with the engine under /gpubox/<VERSION>/ (immutable, pinned: bump VERSION and
// the folder together when the engine changes).
//
//   page -> worker  { id, action:'ping' }
//                   { id, action:'run',  source, kernel, grid, block, shared?, profile?, buffers, args }   one launch
//                   { id, action:'test', source, harness, sampleLimit?, profile? }                       a problem's cases
//                   { id, action:'check', source }                                                       compile only
//   worker -> page  { id, ok:true, ... } | { id, ok:false, error }
//
// A problem's `harness` is the body of a function (H) => ({ cases: [...] }). Each case:
//   { name, hidden?, buffers:[{type:'f32'|'i32', data, read?}],
//     launches:[{kernel, grid, block, shared?, args:[number | {buf:i}]}],
//     expect?:{[bufIndex]: number[]}, tol?:{abs,rel}, check?(outputs)=>null|string, allowErrors? }
// Integers live in the simulator's float32 memory, so 'i32' values are exact below 2^24.
const VERSION = '1.0.0-tt2';
const FILES = [
	'gpu-profiles.js', 'fp16-bf16.js', 'race-detector.js', 'sparse-memory.js', 'topology-model.js',
	'desync-detector.js', 'cuda-transpiler.js', 'cuda-runtime.js', 'validation-harness.js', 'cuda-sim.min.js'
];
const base = new URL('.', self.location.href).href + VERSION + '/';
const t0 = performance.now();
try {
	importScripts(...FILES.map((f) => base + f));
} catch (e) {
	postMessage({ id: -1, ok: false, error: 'Could not load Gpubox: ' + (e && e.message) });
}
const loadMs = performance.now() - t0;
const compileCache = new Map(); // VERSION + source -> compiled program (parse once, run every case)

// ---- helpers handed to problem harnesses ----
function mulberry32(a) {
	return function () {
		a |= 0; a = (a + 0x6d2b79f5) | 0;
		let t = Math.imul(a ^ (a >>> 15), 1 | a);
		t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
		return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
	};
}
const H = {
	rand(n, seed, lo = -1, hi = 1) { const r = mulberry32(seed); return Array.from({ length: n }, () => Math.fround(lo + (hi - lo) * r())); },
	ints(n, seed, lo, hi) { const r = mulberry32(seed); return Array.from({ length: n }, () => lo + Math.floor(r() * (hi - lo + 1))); },
	zeros: (n) => new Array(n).fill(0),
	fill: (n, v) => new Array(n).fill(v),
	range: (n) => Array.from({ length: n }, (_, i) => i),
	ceil: (a, b) => Math.floor((a + b - 1) / b),
	fround: Math.fround,
	// launch helpers: a 1-D launch covering n elements, a 2-D launch covering w x h, a 3-D one covering w x h x d
	l1(kernel, n, args, block = 256, shared = 0) { return { kernel, grid: Math.max(1, Math.floor((n + block - 1) / block)), block, shared, args }; },
	l2(kernel, w, h, args, bx = 16, by = 16) { return { kernel, grid: { x: Math.max(1, Math.floor((w + bx - 1) / bx)), y: Math.max(1, Math.floor((h + by - 1) / by)) }, block: { x: bx, y: by }, args }; },
	l3(kernel, w, h, d, args, bx = 8, by = 4, bz = 4) { return { kernel, grid: { x: Math.ceil(w / bx), y: Math.ceil(h / by), z: Math.ceil(d / bz) }, block: { x: bx, y: by, z: bz }, args }; },
	sum: (a) => a.reduce((x, y) => x + y, 0)
};

// ---- friendly compile errors ----------------------------------------------------------------------
// The simulator translates CUDA C++ to JavaScript, so a typo in the kernel surfaces as a JS error such as
// "Unexpected token 'function'" that says nothing about the learner's code. Before translating, scan the source
// for the mistakes people actually make (unbalanced brackets, a missing semicolon, an unterminated comment or
// string) and report them with the line.
function frame(lines, n) {
	const text = (lines[n - 1] || '').replace(/\t/g, '    ');
	return '\n\n  ' + String(n).padStart(3) + ' | ' + text.trim();
}

function lintSource(source) {
	const lines = source.split('\n');
	const stack = [];
	const close = { ')': '(', ']': '[', '}': '{' };
	const clean = []; // the source with comments blanked and string contents masked, newlines kept
	let line = 1, mode = null, modeLine = 0;
	for (let i = 0; i < source.length; i++) {
		const c = source[i], n = source[i + 1];
		if (c === '\n') { line++; if (mode === 'line') mode = null; clean.push('\n'); continue; }
		if (mode === 'line') { clean.push(' '); continue; }
		if (mode === 'block') { if (c === '*' && n === '/') { mode = null; clean.push(' ', ' '); i++; } else clean.push(' '); continue; }
		if (mode === '"' || mode === "'") {
			if (c === '\\') { clean.push('x', 'x'); i++; continue; }
			if (c === mode) { mode = null; clean.push(c); } else clean.push('x');
			continue;
		}
		if (c === '/' && n === '/') { mode = 'line'; clean.push(' ', ' '); i++; continue; }
		if (c === '/' && n === '*') { mode = 'block'; modeLine = line; clean.push(' ', ' '); i++; continue; }
		if (c === '"' || c === "'") { mode = c; modeLine = line; clean.push(c); continue; }
		clean.push(c);
		if (c === '(' || c === '[' || c === '{') stack.push({ c, line });
		else if (c === ')' || c === ']' || c === '}') {
			const top = stack.pop();
			if (!top) return { line, message: "Unexpected '" + c + "': there is no matching '" + close[c] + "' before it." };
			if (top.c !== close[c]) {
				const want = { '(': ')', '[': ']', '{': '}' }[top.c];
				return { line: top.line, message: "The '" + top.c + "' opened here is not closed: expected '" + want + "' but line " + line + " has '" + c + "' first." };
			}
		}
	}
	if (mode === 'block') return { line: modeLine, message: "This '/*' comment is never closed with '*/'." };
	if (mode === '"' || mode === "'") return { line: modeLine, message: 'This string or character literal is never closed.' };
	if (stack.length) {
		const top = stack[stack.length - 1];
		const want = { '(': ')', '[': ']', '{': '}' }[top.c];
		return { line: top.line, message: "The '" + top.c + "' opened here is never closed: add a '" + want + "'." };
	}
	// A statement that does not end in ';'. Only inside a function body, and only when the line ends like a
	// finished statement (a word, number, ']' or a balanced call) and the next line clearly starts a new one.
	const code = clean.join('').split('\n').map((l) => l.trim());
	let depth = 0;
	for (let li = 0; li < code.length; li++) {
		const t = code[li];
		const here = depth;
		for (const ch of t) { if (ch === '{') depth++; else if (ch === '}') depth--; }
		if (!t || here === 0 || t.startsWith('#') || t.endsWith('\\')) continue;
		let next = '';
		for (let k = li + 1; k < code.length; k++) if (code[k]) { next = code[k]; break; }
		if (!next) continue;
		const last = t[t.length - 1];
		const continues = /^[.\[\]),;?:+\-*\/%=&|^<>]/.test(next) && !/^(\+\+|--)/.test(next);
		const control = /^(\}\s*)?(if|for|while|switch|else|do|case|default)\b/.test(t) || /(^|\W)(else|do)$/.test(t) || /^[A-Za-z_]\w*\s*:$/.test(t);
		const opens = (t.match(/\(/g) || []).length, closes = (t.match(/\)/g) || []).length;
		const endsLikeStatement = /[A-Za-z0-9_\]'"]/.test(last) || (last === ')' && opens >= closes && /[=\w]\s*\(/.test(t));
		if (endsLikeStatement && !control && !continues && !next.startsWith('{') && !/^(template|__global__|__device__|__host__|struct|class|enum|typedef)\b/.test(t))
			return { line: li + 1, message: "This line does not end with ';' (the next line starts a new statement)." };
	}
	return null;
}

function compileError(lines, line, message) {
	return new Error('Compile error' + (line ? ' (line ' + line + ')' : '') + ': ' + message + (line ? frame(lines, line) : ''));
}

// `source` (optional) lets the message say on which line a name first appears.
function friendlyJsError(e, source) {
	const msg = String((e && e.message) || e);
	let m = /^(\w+) is not defined/.exec(msg);
	if (m) {
		let where = '';
		if (source) {
			const at = source.split('\n').findIndex((l) => new RegExp('\\b' + m[1] + '\\b').test(l));
			if (at >= 0) where = ' It first appears on line ' + (at + 1) + '.';
		}
		return "'" + m[1] + "' is used but never declared (check the spelling, or declare it before using it)." + where;
	}
	m = /Unexpected (token|identifier|end of input|string|number)/.exec(msg);
	if (m) return 'the simulator could not parse the kernel (' + msg + '). This usually means a missing or extra bracket, parenthesis or semicolon, or a C++ feature the simulator does not support.';
	return msg;
}

function compileOnce(source) {
	const key = VERSION + '\u0000' + source;
	let prog = compileCache.get(key);
	let cached = true;
	if (!prog) {
		cached = false;
		const lines = source.split('\n');
		const lint = lintSource(source);
		if (lint) throw compileError(lines, lint.line, lint.message);
		prog = self.Gpubox.compile(source);
		if (prog.analysis && prog.analysis.success === false)
			throw new Error('Compile error: this kernel uses something the simulator does not support: ' + JSON.stringify(prog.analysis.unsupportedFeatures));
		if (prog.errors && prog.errors.length) throw new Error('Compile error: ' + prog.errors.join('; '));
		try {
			new Function('__rt', prog.transpiledCode);
		} catch (e) {
			throw new Error('Compile error: ' + friendlyJsError(e));
		}
		compileCache.set(key, prog);
	}
	return { prog, cached };
}

function kernelFn(prog, name) {
	const fn = new Function('__rt', prog.transpiledCode + '; return typeof __kernel_' + name + " === 'function' ? __kernel_" + name + ' : null;')();
	if (!fn) throw new Error('Kernel "' + name + '" was not found. Keep the function name and signature from the starter code.');
	return fn;
}

// Runs one case on a fresh simulator. Returns { outputs, counters, diagnostics, ms, profile }.
function runCase(prog, c, profile) {
	const sim = self.Gpubox.createSimulator({ gpuProfile: profile, raceDetection: true });
	const bufs = c.buffers.map((b) => {
		const arr = Float32Array.from(b.data); // ints are stored as float32 values
		const p = sim.allocate(Math.max(arr.byteLength, 16));
		if (arr.byteLength) sim.memcpy(p, arr, arr.byteLength, 'H2D');
		return { p, n: arr.length, type: b.type, read: b.read };
	});
	const start = performance.now();
	for (const l of c.launches) {
		sim.launch(kernelFn(prog, l.kernel), l.grid, l.block, l.shared || 0, ...l.args.map((a) => (a && typeof a === 'object' ? bufs[a.buf].p : a)));
	}
	const ms = performance.now() - start;
	const outputs = {};
	bufs.forEach((b, i) => {
		if (!b.read) return;
		const out = new Float32Array(b.n);
		if (b.n) sim.memcpy(out, b.p, b.n * 4, 'D2H');
		outputs[i] = Array.from(out, (v) => (b.type === 'i32' ? Math.round(v) : v));
	});
	return { outputs, counters: sim.getCounters().toJSON(), diagnostics: sim.getDiagnostics(), ms, profile };
}

const fmt = (v) => (Number.isInteger(v) ? String(v) : Number(v.toPrecision(6)).toString());
const head = (arr, n = 8) => '[' + arr.slice(0, n).map(fmt).join(', ') + (arr.length > n ? ', … (' + arr.length + ' values)' : '') + ']';

function compare(expect, outputs, tol) {
	const abs = tol && tol.abs !== undefined ? tol.abs : 1e-5, rel = tol && tol.rel !== undefined ? tol.rel : 1e-4;
	for (const k of Object.keys(expect)) {
		const exp = expect[k], got = outputs[k];
		if (!got) return { ok: false, message: 'Buffer ' + k + ' was not read back', expected: head(exp), actual: '(none)' };
		for (let i = 0; i < exp.length; i++) {
			const e = exp[i], g = got[i];
			const bothNaN = Number.isNaN(e) && Number.isNaN(g);
			if (bothNaN || e === g) continue;
			if (!(Math.abs(e - g) <= abs + rel * Math.abs(e)))
				return { ok: false, message: 'output[' + i + '] is ' + fmt(g) + ', expected ' + fmt(e), expected: head(exp.slice(Math.max(0, i - 2))), actual: head(got.slice(Math.max(0, i - 2))), index: i };
		}
	}
	return { ok: true };
}

function report(r) {
	const c = r.counters, pct = (x) => (x * 100).toFixed(0) + '%';
	const lines = [
		'GPU model: ' + r.profile + ' (simulated; times are a model, not a measurement)',
		'Global memory: ' + c.globalLoadBytes + ' B read, ' + c.globalStoreBytes + ' B written, ' + c.globalTransactions + ' transactions (' + c.idealGlobalTransactions + ' ideal) -> coalescing ' + pct(c.coalescingEfficiency)
	];
	if (c.sharedLoads + c.sharedStores) {
		lines.push('Shared memory: ' + c.sharedLoads + ' loads, ' + c.sharedStores + ' stores, ' + c.bankConflicts + ' bank-conflict replays');
		if (c.bankAccesses) {
			const peak = Math.max(1, ...c.bankAccesses), shade = ' \u2581\u2582\u2583\u2584\u2585\u2586\u2587\u2588';
			lines.push('Banks 0..31 (words touched): ' + c.bankAccesses.map((a) => shade[Math.round((a / peak) * 8)]).join('') + '   peak ' + peak + ' words in one bank');
			const rpeak = Math.max(...c.bankReplays);
			if (rpeak > 0) lines.push('Bank-conflict heat 0..31 (replays):   ' + c.bankReplays.map((a) => shade[Math.round((a / rpeak) * 8)]).join('') + '   worst bank ' + rpeak + ' replays');
			const hot = c.bankReplays.map((r, b) => [b, r]).filter((x) => x[1] > 0).sort((a, b) => b[1] - a[1]).slice(0, 6);
			lines.push(hot.length ? 'Conflicted banks: ' + hot.map((x) => 'bank ' + x[0] + ' (' + x[1] + ' replays)').join(', ') + '. Pad the tile (for example [32][33]) so a column spreads over all 32 banks.' : 'No bank conflicts: every warp access spreads over distinct banks.');
		}
	}
	lines.push('Branches: ' + c.divergentBranches + ' of ' + c.branchEvents + ' warp-level branches diverged');
	if (c.atomicOps) lines.push('Atomics: ' + c.atomicOps + ' (worst contention on one address: ' + c.atomicMaxContention + ')');
	lines.push('FLOPs (static estimate): ' + c.flopCount + '; modelled time ' + c.estimatedTimeMs.toFixed(4) + ' ms; occupancy ' + pct(c.occupancy));
	return lines.join('\n');
}

// A whole host program (multi-GPU problems): run main() on N simulated devices, judge what it printed.
function runPrograms(m, spec, T0) {
	const profile = m.profile || spec.profile || 'A100';
	const results = spec.programs.filter((p) => !m.sampleLimit || !p.hidden).map((p) => {
		const res = { name: p.name, hidden: !!p.hidden };
		try {
			const r = self.Gpubox.run(m.source, { gpuProfile: profile, numDevices: p.devices || 2 });
			const text = (r.diagnostics || []).filter((d) => d.type === 'printf').map((d) => String(d.message).replace(/\\n/g, '\n')).join('');
			const per = (r.counters && r.counters.perDevice) || [];
			const n = p.devices || 2;
			const cluster = per.length ? ['Cluster of ' + n + ' simulated ' + profile + ' GPUs: ' + ((r.counters && r.counters.ncclOps) || 0) + ' collective calls, ' + ((r.counters && r.counters.crossGpuBytes) || 0) + ' bytes over the interconnect in total']
				.concat(per.map((d, i) => '  GPU ' + i + ': ' + (d.ncclOps || 0) + ' collective call(s), ' + (d.crossGpuBytes || 0) + ' bytes sent/received')).join('\n') : '';
			res.report = 'Status: ' + r.status + (cluster ? '\n' + cluster : '') + '\n--- program output ---\n' + text.trim();
			const err = (r.diagnostics || []).find((d) => d.type !== 'printf' && (d.type === 'error' || /Error$/.test(d.category || '') || /Error$/.test(d.type || '')));
			if (r.status !== 'PASS' || err) {
				res.passed = false;
				res.error = err ? err.message : 'The program ended with status ' + r.status;
				return res;
			}
			const msg = p.check ? p.check(r, text) : null;
			res.passed = !msg;
			if (msg) res.error = msg;
		} catch (e) { res.passed = false; res.error = String((e && e.message) || e); }
		return res;
	});
	return { results, cached: false, totalMs: performance.now() - T0 };
}

// Running code from a message is this worker's job: the learner's kernel is compiled and executed here, in the
// learner's own browser, inside a Worker with no DOM, cookies or storage. The harness is the problem's own test
// script, sent by the page from the site's bundled problem data. It is only accepted as a bounded string.
const MAX_HARNESS_CHARS = 200000;
function loadSpec(harness) {
	if (typeof harness !== 'string' || harness.length > MAX_HARNESS_CHARS) throw new Error('Invalid test harness');
	return new Function('H', harness)(H);
}

function runTest(m) {
	const T0 = performance.now();
	const spec = loadSpec(m.harness);
	if (spec.programs) return runPrograms(m, spec, T0);
	const { prog, cached } = compileOnce(m.source);
	const profile = m.profile || spec.profile || 'A100';
	let cases = spec.cases.filter((c) => !m.sampleLimit || !c.hidden);
	if (m.sampleLimit) cases = cases.slice(0, m.sampleLimit);
	const results = cases.map((c) => {
		const res = { name: c.name, hidden: !!c.hidden };
		try {
			const r = runCase(prog, c, profile);
			const errors = r.diagnostics.filter((d) => d.type === 'error' || /Error$/.test(d.category || ''));
			res.report = report(r);
			res.counters = r.counters;
			if (errors.length && !c.allowErrors) {
				res.passed = false;
				const d = errors[0];
				res.error = friendlyJsError(d.message, m.source) + (d.location ? ' (block ' + (d.location.block ? d.location.block.x : '?') + ', thread ' + (d.location.thread ? d.location.thread.x : '?') + ')' : d.block ? ' (block ' + d.block.x + ', thread ' + (d.thread ? d.thread.x : '?') + ')' : '');
				return res;
			}
			let verdict = { ok: true };
			if (c.expect) verdict = compare(c.expect, r.outputs, c.tol);
			if (verdict.ok && c.check) {
				const msg = c.check(r.outputs, r.counters, r.diagnostics);
				if (msg) verdict = { ok: false, message: msg };
			}
			res.passed = verdict.ok;
			if (!verdict.ok) { res.error = verdict.message; res.expected = verdict.expected; res.actual = verdict.actual; }
		} catch (e) {
			res.passed = false;
			const msg = String((e && e.message) || e);
			res.error = /OOB/.test(msg) ? 'Out-of-bounds memory access: ' + msg + '. Is a bounds check missing?' : friendlyJsError(e, m.source);
		}
		return res;
	});
	return { results, cached, totalMs: performance.now() - T0 };
}

self.onmessage = (ev) => {
	// A dedicated worker only ever hears from the page that created it (its origin is the empty string); a message
	// carrying some other origin did not come from that page, so it is ignored.
	if (ev.origin && ev.origin !== self.location.origin) return;
	const m = ev.data;
	try {
		if (m.action === 'ping') return postMessage({ id: m.id, ok: true, version: VERSION, loadMs });
		if (m.action === 'check') {
			const { prog } = compileOnce(m.source);
			return postMessage({ id: m.id, ok: true, kernels: prog.kernelNames || [] });
		}
		if (m.action === 'test') return postMessage({ id: m.id, ok: true, ...runTest(m) });
		if (m.action === 'run') {
			const { prog, cached } = compileOnce(m.source);
			const r = runCase(prog, { buffers: m.buffers, launches: [{ kernel: m.kernel, grid: m.grid, block: m.block, shared: m.shared, args: m.args }] }, m.profile || 'A100');
			return postMessage({ id: m.id, ok: true, outputs: r.outputs, counters: r.counters, diagnostics: r.diagnostics, timings: { cached, ms: r.ms } });
		}
	} catch (e) {
		postMessage({ id: m.id, ok: false, error: String((e && e.message) || e) });
	}
};
