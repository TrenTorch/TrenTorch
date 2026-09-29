import { createActionButton } from '../components/visualizers/ActionButton.js';
import { createCanvasPlot } from '../components/visualizers/CanvasPlot.js';
import { createSlider } from '../components/visualizers/Slider.js';
import { createStatsPanel } from '../components/visualizers/StatsPanel.js';
import { seededRandom } from '../components/visualizers/seededRandom.js';
import { drawHeatmapGrid } from '../components/visualizers/HeatmapGrid.js';
import { drawMemoryBlockGrid } from '../components/visualizers/MemoryBlockGrid.js';
import { drawTimeline } from '../components/visualizers/Timeline.js';
import { drawTrieDiagram } from '../components/visualizers/TrieDiagram.js';
import { runPythonBenchmark } from './python-benchmarks.js';
import { systemsVisualizerIdSet } from './systems-visualizer-ids.js';

const accent = '#fb7185';
const blue = '#60a5fa';
const green = '#34d399';
const orange = '#fbbf24';
const red = '#f87171';

/** @type {Record<string, string>} */
const captions = {
	'inf-attn-scaled-dot-product':
		'Toggle √d scaling and see how it keeps attention from collapsing onto one token.',
	'inf-attn-multi-head':
		'Each head learns a different attention pattern before their outputs are concatenated.',
	'inf-attn-multi-query':
		'Share one K/V pair across query heads and reduce cache memory by the number of heads.',
	'inf-attn-grouped-query':
		'Move from one shared K/V group to one group per query head and compare cache size.',
	'inf-attn-multi-head-latent':
		'Compress the cached keys and values to a low-rank latent, then compare the footprint.',
	'inf-kv-rope-decoding':
		'Shift both positions equally: the relative angle and encoded dot product remain unchanged.',
	'inf-kv-autoregressive-cache':
		'Without a KV cache, each new token recomputes attention over the entire prefix.',
	'inf-kv-memory-footprint':
		'Scale sequence length and batch size to see which attention variant fits in memory.',
	'inf-kv-paged-attention':
		'Allocate cache blocks only when sequences need them; finish a sequence to free its pages.',
	'inf-kv-prefix-cache':
		'Requests with a shared prefix reuse cached tokens and compute only the new suffix.',
	'inf-quant-int8-symmetric':
		'Compare floating-point values with their nearest INT8 grid points and reconstruction error.',
	'inf-quant-per-channel':
		'Per-channel scales prevent one large row from wasting precision for every other row.',
	'inf-quant-int4-groupwise':
		'Smaller quantization groups reduce error but require more scale metadata.',
	'inf-quant-fp8-blockwise':
		'Compare uniform INT8 steps with FP8 precision concentrated around smaller values.',
	'inf-quant-roofline':
		'Increase batch size and watch decode arithmetic intensity move toward compute-bound.',
	'inf-batch-latency-percentiles':
		'Add slow-tail requests and compare P99 with the mean and median.',
	'inf-batch-serving-metrics-ttft-tpot-itl':
		'Separate the initial wait for the first token from the gaps between later tokens.',
	'inf-batch-dynamic-request-batching':
		'Wider batching windows trade higher request wait time for larger, more efficient batches.',
	'inf-batch-continuous-batching':
		'Continuous batching refills a slot as soon as a short request finishes.',
	'inf-batch-chunked-prefill':
		'Interleave chunks of long prompts with decode steps to reduce stalls for active requests.',
	'systems-perf-timing-decorator':
		'Run repeated timed work and compare real in-browser durations, including warm-up effects.',
	'systems-perf-parameter-counting':
		'Adjust layer dimensions and see how weight and bias counts contribute to the total.',
	'systems-perf-memory-footprint-estimation':
		'Compare parameter, gradient, optimizer, and activation memory under different settings.',
	'systems-perf-flops-estimation':
		'Change layer shapes to compare parameter count with the work performed per forward pass.',
	'systems-perf-checkpointing':
		'Simulate a crash and see how many steps since the last checkpoint must be repeated.',
	'systems-perf-quantize-float32-to-int8':
		'Move a value and see it snap to an INT8 grid point, with quantization error shown live.',
	'systems-perf-dequantize-int8-to-float32':
		'Reconstruct a float from its quantized integer and inspect the round-trip error.',
	'systems-perf-quantize-weight-matrix-tradeoff':
		'Compare INT8 storage savings with the output error introduced by quantizing a matrix.',
	'systems-perf-fp16-bf16-representable-range':
		'Move across the value range and compare where FP16 and BF16 underflow or overflow.',
	'systems-perf-loss-scaling':
		'Scale tiny gradients into FP16 range, then unscale them before the optimizer step.',
	'systems-perf-autocast-concept':
		'Autocast lowers precision selectively; numerically sensitive operations stay in FP32.',
	'systems-perf-magnitude-pruning':
		'Raise sparsity and see small-magnitude weights removed from the matrix.',
	'systems-perf-iterative-pruning-schedule':
		'Compare one large pruning step with gradual pruning and fine-tuning rounds.',
	'systems-perf-knowledge-distillation':
		'Soften the teacher distribution and see the student’s KL divergence respond.',
	'systems-perf-vectorize-naive-loop':
		'Run a Python loop and equivalent NumPy operation in Pyodide on the same array and compare real timings.',
	'systems-perf-kernel-fusion':
		'Fusing elementwise passes avoids an intermediate memory round-trip.',
	'systems-perf-roofline-model':
		'Fusion moves memory-bound work toward higher arithmetic intensity on the roofline.',
	'systems-perf-real-kernels-cuda-triton':
		'Change block size and inspect the launched blocks, threads, and wasted lanes.',
	'systems-perf-torch-compile-graph-compilation':
		'Compiled graphs reduce per-operation dispatch gaps by grouping operations.',
	'systems-perf-torchscript-onnx-export':
		'Export a model graph and compare the conceptual serving stacks.'
};

/**
 * @typedef {{ primary: number; secondary: number; n: number; step: number; mode: string; samples: number[]; blocks: number[]; events: number[]; running: boolean; result: string }} State
 */

/** @param {CanvasRenderingContext2D} context @param {number} width @param {number} height */
function clear(context, width, height) {
	context.clearRect(0, 0, width, height);
	context.fillStyle = '#09090b';
	context.fillRect(0, 0, width, height);
	context.font = '12px ui-monospace, SFMono-Regular, Menlo, monospace';
	context.textBaseline = 'middle';
	context.fillStyle = '#d4d4d8';
}

/** @param {CanvasRenderingContext2D} context @param {string} text @param {number} x @param {number} y @param {string} [color] */
function label(context, text, x, y, color = '#d4d4d8') {
	context.fillStyle = color;
	context.fillText(text, x, y);
}

/** @param {CanvasRenderingContext2D} context @param {number} x @param {number} y @param {number} width @param {number} height @param {string} color */
function box(context, x, y, width, height, color) {
	context.fillStyle = color;
	context.fillRect(x, y, width, height);
	context.strokeStyle = 'rgba(255,255,255,.12)';
	context.strokeRect(x, y, width, height);
}

/** @param {string} id @param {State} state @param {number} width @param {number} height @param {CanvasRenderingContext2D} context @param {number} seed */
function draw(id, state, width, height, context, seed) {
	clear(context, width, height);
	const random = seededRandom(seed);
	const pad = 28;

	if (id.startsWith('inf-attn-')) {
		if (
			id === 'inf-attn-multi-query' ||
			id === 'inf-attn-grouped-query' ||
			id === 'inf-attn-multi-head-latent'
		) {
			const heads = Math.max(1, Math.round(state.primary));
			const groups =
				id === 'inf-attn-multi-query'
					? 1
					: id === 'inf-attn-multi-head-latent'
						? Math.max(1, Math.round(state.secondary))
						: Math.min(heads, Math.max(1, Math.round(state.secondary)));
			const barY = 68;
			const barH = 34;
			const totalW = width - pad * 2;
			label(context, 'K/V cache blocks per token', pad, 34);
			for (let index = 0; index < heads; index++) {
				const x = pad + (index * totalW) / heads;
				const owner = Math.floor((index * groups) / heads);
				box(
					context,
					x,
					barY,
					Math.max(4, totalW / heads - 3),
					barH,
					`hsl(${205 + owner * 28} 76% 52%)`
				);
			}
			for (let group = 0; group < groups; group++) {
				label(
					context,
					`KV group ${group + 1}`,
					pad + ((group + 0.5) * totalW) / groups - 28,
					barY + 62,
					blue
				);
			}
			const ratio = groups / heads;
			box(context, pad, 170, totalW, 25, '#27272a');
			box(context, pad, 170, totalW * ratio, 25, accent);
			label(
				context,
				`${groups} KV groups / ${heads} query heads · ${Math.round(ratio * 100)}% of MHA cache`,
				pad,
				218
			);
			label(context, 'MHA', pad, 260, blue);
			box(context, pad + 42, 250, totalW - 42, 18, blue);
			label(context, 'MQA', pad, 295, green);
			box(context, pad + 42, 285, Math.max(8, (totalW - 42) / heads), 18, green);
			return;
		}

		const tokens = Math.max(
			2,
			Math.round(id === 'inf-attn-scaled-dot-product' ? state.primary : state.n)
		);
		const cell = Math.min((width - pad * 2) / tokens, (height - 122) / tokens, 46);
		const startX = (width - cell * tokens) / 2;
		const startY = 42;
		const selected = Math.min(tokens - 1, Math.max(0, Math.round(state.step)));
		label(
			context,
			id === 'inf-attn-scaled-dot-product'
				? 'QKᵀ scores → scaled softmax weights'
				: 'Per-head attention weights',
			pad,
			20
		);
		const weights = [];
		for (let row = 0; row < tokens; row++) {
			let total = 0;
			const scores = Array.from(
				{ length: tokens },
				() => random() * (state.mode === 'unscaled' ? 7 : 2) - 1
			);
			for (const score of scores) total += Math.exp(score);
			weights.push(scores.map((score) => Math.exp(score) / total));
			label(context, `q${row + 1}`, startX - 23, startY + row * cell + cell / 2);
		}
		drawHeatmapGrid(context, {
			x: startX,
			y: startY,
			width: cell * tokens,
			height: cell * tokens,
			values: weights,
			selectedRow: selected
		});
		label(
			context,
			'Click Step to inspect another query row',
			pad,
			startY + tokens * cell + 24,
			'#a1a1aa'
		);
		if (id === 'inf-attn-scaled-dot-product') {
			const outputY = height - 42;
			label(context, 'selected attention × V → output', pad, outputY - 8, green);
			for (let token = 0; token < tokens; token++) {
				const value = weights[selected][token];
				box(
					context,
					pad + token * ((width - pad * 2) / tokens),
					outputY + 5,
					Math.max(2, ((width - pad * 2) / tokens - 3) * value),
					12,
					green
				);
			}
		}
		if (id === 'inf-attn-multi-head') {
			for (let head = 0; head < 4; head++) {
				const y = height - 76 + head * 12;
				box(
					context,
					pad + head * 12,
					y,
					(width - pad * 2) * (0.42 + head * 0.1),
					8,
					[accent, blue, green, orange][head]
				);
			}
			label(context, 'head outputs → concatenated embedding', pad, height - 22);
		}
		return;
	}

	if (id.startsWith('inf-kv-')) {
		if (id === 'inf-kv-rope-decoding') {
			const cx = width / 2;
			const cy = height / 2;
			const radius = Math.min(height, width) * 0.28;
			context.beginPath();
			context.arc(cx, cy, radius, 0, Math.PI * 2);
			context.strokeStyle = '#52525b';
			context.stroke();
			const first = state.primary * 0.07;
			const second = (state.primary + state.secondary) * 0.07;
			for (const [angle, color, text] of /** @type {Array<[number, string, string]>} */ ([
				[first, accent, 'm'],
				[second, blue, 'n']
			])) {
				context.beginPath();
				context.moveTo(cx, cy);
				context.lineTo(cx + Math.cos(angle) * radius, cy - Math.sin(angle) * radius);
				context.strokeStyle = color;
				context.lineWidth = 3;
				context.stroke();
				label(
					context,
					text,
					cx + Math.cos(angle) * radius + 8,
					cy - Math.sin(angle) * radius,
					color
				);
			}
			label(
				context,
				`relative angle: ${(state.secondary * 0.07).toFixed(2)} rad`,
				pad,
				height - 24
			);
			return;
		}
		if (id === 'inf-kv-prefix-cache') {
			const levels = [
				[{ x: width / 2, text: 'root' }],
				[
					{ x: width * 0.32, text: 'system' },
					{ x: width * 0.68, text: 'other' }
				],
				[
					{ x: width * 0.24, text: 'You' },
					{ x: width * 0.42, text: 'Help' },
					{ x: width * 0.7, text: 'New' }
				],
				[
					{ x: width * 0.24, text: 'cached' },
					{ x: width * 0.42, text: 'cached' },
					{ x: width * 0.7, text: 'miss' }
				]
			];
			drawTrieDiagram(context, {
				width,
				height,
				levels: levels.map((nodes) => nodes.map(({ x, text }) => ({ x, label: text }))),
				hitDepth: 2
			});
			label(context, `tokens reused: ${Math.round(state.n * 0.6)}`, pad, height - 18, green);
			return;
		}
		if (id === 'inf-kv-paged-attention') {
			const count = Math.max(8, Math.min(30, Math.round(state.n / 4)));
			const owners = Array.from({ length: count }, (_, index) =>
				index < Math.min(count, Math.round(state.step)) ? String(index % 3) : null
			);
			label(context, 'Physical KV block pool', pad, 28);
			drawMemoryBlockGrid(context, { x: pad, y: 55, width: width - pad * 2, blocks: owners });
			label(
				context,
				`used ${Math.round(state.step)} · free ${count - Math.round(state.step)}`,
				pad,
				height - 18
			);
			return;
		}
		if (id === 'inf-kv-autoregressive-cache') {
			const steps = Math.max(2, Math.min(12, Math.round(state.secondary)));
			drawTimeline(context, {
				x: pad,
				y: 55,
				width: width - pad * 2,
				height: height - 85,
				duration: steps + 2,
				lanes: ['generation'],
				events: [
					{ label: 'prefill', start: 0, duration: 2, lane: 0, color: orange },
					...Array.from({ length: steps }, (_, index) => ({
						label: `t${index + 1}`,
						start: index + 2,
						duration: state.mode === 'recompute' ? 0.8 + index / 3 : 0.55,
						lane: 0,
						color: state.mode === 'recompute' ? red : blue
					}))
				]
			});
			label(context, 'prefill → autoregressive decode', pad, 30, orange);
			return;
		}
		const count = Math.max(4, Math.min(20, Math.round(state.n / 5)));
		label(
			context,
			id === 'inf-kv-paged-attention' ? 'Physical KV block pool' : 'Prompt prefill → token decode',
			pad,
			28
		);
		for (let index = 0; index < count; index++) {
			const x = pad + (index % 10) * ((width - pad * 2) / 10);
			const y = 55 + Math.floor(index / 10) * 42;
			const active = index < Math.min(count, Math.round(state.step));
			box(
				context,
				x,
				y,
				Math.max(20, (width - pad * 2) / 10 - 5),
				28,
				active ? [accent, blue, green][index % 3] : '#27272a'
			);
			label(
				context,
				active ? `S${(index % 3) + 1}` : 'free',
				x + 3,
				y + 42,
				active ? '#fafafa' : '#71717a'
			);
		}
		const bars = Math.min(12, Math.max(2, Math.round(state.secondary)));
		for (let index = 0; index < bars; index++) {
			const x = pad + index * ((width - pad * 2) / bars);
			const h =
				id === 'inf-kv-autoregressive-cache' && state.mode === 'recompute' ? 32 + index * 12 : 30;
			box(
				context,
				x,
				height - h - 26,
				Math.max(4, (width - pad * 2) / bars - 3),
				h,
				state.mode === 'recompute' ? red : blue
			);
		}
		label(
			context,
			id === 'inf-kv-memory-footprint' ? 'MHA  ·  GQA  ·  MQA  ·  MLA' : 'decode steps',
			pad,
			height - 12
		);
		return;
	}

	if (id.startsWith('inf-quant-') || id.includes('quantize') || id.includes('dequantize')) {
		const mid = height * 0.53;
		context.beginPath();
		context.moveTo(pad, mid);
		context.lineTo(width - pad, mid);
		context.strokeStyle = '#52525b';
		context.stroke();
		for (let index = 0; index < 18; index++) {
			const x = pad + (index * (width - pad * 2)) / 17;
			context.beginPath();
			context.moveTo(x, mid - 6);
			context.lineTo(x, mid + 6);
			context.strokeStyle = '#71717a';
			context.stroke();
		}
		const point = pad + (width - pad * 2) * ((Math.sin(state.primary) + 1) / 2);
		context.beginPath();
		context.arc(point, mid - 25, 7, 0, Math.PI * 2);
		context.fillStyle = accent;
		context.fill();
		context.beginPath();
		context.moveTo(point, mid - 16);
		context.lineTo(
			pad + Math.round((point - pad) / ((width - pad * 2) / 17)) * ((width - pad * 2) / 17),
			mid - 2
		);
		context.strokeStyle = orange;
		context.stroke();
		label(
			context,
			id === 'inf-quant-fp8-blockwise'
				? `${state.mode === 'fp8' ? 'FP8 E4M3' : 'INT8'} grid → reconstructed values`
				: 'float values → quantization grid → reconstruction',
			pad,
			26
		);
		for (let row = 0; row < 7; row++) {
			for (let col = 0; col < 16; col++) {
				const error = Math.abs(Math.sin((row + 1) * (col + 2) + state.primary)) * state.secondary;
				box(
					context,
					pad + col * ((width - pad * 2) / 16),
					height - 92 + row * 10,
					(width - pad * 2) / 16 - 2,
					8,
					`rgba(251,113,133,${Math.min(0.95, error / 4)})`
				);
			}
		}
		label(context, 'illustrative quantization error', pad, height - 14, '#a1a1aa');
		return;
	}

	if (id.startsWith('inf-batch-')) {
		const lanes = 4;
		const events = Math.max(4, Math.min(16, Math.round(state.n / 4)));
		drawTimeline(context, {
			x: 4,
			y: 46,
			width: width - 8,
			height: Math.min(208, height - 78),
			duration: events,
			lanes: Array.from({ length: lanes }, (_, lane) => `req ${lane + 1}`),
			events: Array.from({ length: lanes }, (_, lane) =>
				Array.from({ length: events }, (_, event) => ({
					label: '',
					start: event + lane * 0.06,
					duration: 0.42,
					lane,
					color: event < state.step ? [accent, blue, green, orange][lane] : '#3f3f46'
				}))
			).flat()
		});
		label(
			context,
			id.includes('latency')
				? 'sorted request latency distribution'
				: 'request arrival and service timeline',
			pad,
			22
		);
		label(context, `completed steps: ${Math.round(state.step)}`, pad, height - 18, green);
		return;
	}

	if (id.includes('roofline')) {
		const left = pad + 22;
		const bottom = height - 45;
		context.beginPath();
		context.moveTo(left, bottom);
		context.lineTo(width - pad, bottom);
		context.moveTo(left, bottom);
		context.lineTo(left, 30);
		context.strokeStyle = '#71717a';
		context.stroke();
		context.beginPath();
		context.moveTo(left, bottom);
		context.lineTo(width * 0.53, height * 0.28);
		context.lineTo(width - pad, height * 0.28);
		context.strokeStyle = green;
		context.lineWidth = 3;
		context.stroke();
		for (const [x, y, color, name] of /** @type {Array<[number, number, string, string]>} */ ([
			[
				left +
					70 +
					state.primary * 8 +
					(id === 'systems-perf-roofline-model' && state.mode === 'on' ? 80 : 0),
				bottom - 60,
				blue,
				'decode'
			],
			[width * 0.72, height * 0.43, orange, 'prefill']
		])) {
			context.beginPath();
			context.arc(x, y, 7, 0, Math.PI * 2);
			context.fillStyle = color;
			context.fill();
			label(context, name, x + 10, y, color);
		}
		label(context, 'arithmetic intensity (FLOPs / byte)', left + 20, height - 17);
		return;
	}

	if (id.includes('timing')) {
		const values = state.samples;
		const max = Math.max(...values, 0.01);
		label(context, 'measured Python call duration · Pyodide (ms)', pad, 28);
		if (values.length === 0) {
			label(context, 'Run both to record a real timing sample', pad, height / 2, '#a1a1aa');
			return;
		}
		values.forEach((value, index) => {
			const barWidth = (width - pad * 2) / values.length - 6;
			const x = pad + (index * (width - pad * 2)) / values.length;
			const barHeight = ((height - 100) * value) / max;
			box(context, x, height - 44 - barHeight, barWidth, barHeight, index === 0 ? orange : blue);
			label(context, `${value.toFixed(2)}ms`, x, height - 30, '#a1a1aa');
		});
		return;
	}
	if (id.includes('vectorize')) {
		const max = Math.max(...state.samples, 0.01);
		label(context, 'Python loop vs NumPy · measured duration (ms)', pad, 28);
		[
			{ name: 'loop', value: state.samples[0] ?? 0, color: orange },
			{ name: 'NumPy', value: state.samples[1] ?? 0, color: blue }
		].forEach(({ name, value, color }, index) => {
			const x = width * (index === 0 ? 0.28 : 0.62);
			const barHeight = value ? ((height - 100) * value) / max : 0;
			box(context, x, height - 44 - barHeight, width * 0.18, barHeight, color);
			label(
				context,
				`${name}: ${value ? `${value.toFixed(2)}ms` : 'run to measure'}`,
				x,
				height - 25,
				color
			);
		});
		return;
	}

	if (id.includes('attention') || id.includes('autocast') || id.includes('distillation')) {
		const columns = Math.min(8, Math.max(3, Math.round(state.n / 10)));
		for (let row = 0; row < 5; row++) {
			const y = 50 + row * 35;
			for (let column = 0; column < columns; column++) {
				const x = pad + column * ((width - pad * 2) / columns);
				box(
					context,
					x,
					y,
					(width - pad * 2) / columns - 4,
					25,
					row < 3 ? [blue, accent, green][row] : '#52525b'
				);
			}
		}
		label(
			context,
			state.mode === 'off' ? 'autocast off · FP32' : 'matmul / conv → softmax → loss',
			pad,
			25
		);
		return;
	}

	if (id.includes('fp16-bf16-representable-range')) {
		const rangeStart = pad + 32;
		const rangeWidth = width - rangeStart - pad;
		const rows = [
			{ label: 'FP32', min: -45, max: 38 },
			{ label: 'BF16', min: -41, max: 38 },
			{ label: 'FP16', min: -7, max: 4.8 }
		];
		rows.forEach(({ label: format, min, max }, index) => {
			const y = 76 + index * 66;
			label(context, format, pad, y + 7);
			box(context, rangeStart, y, rangeWidth, 14, '#27272a');
			box(
				context,
				rangeStart + ((min + 45) / 83) * rangeWidth,
				y,
				((max - min) / 83) * rangeWidth,
				14,
				format === 'FP16' ? orange : blue
			);
			const markerX = rangeStart + ((state.primary + 45) / 83) * rangeWidth;
			box(
				context,
				markerX - 2,
				y - 5,
				4,
				24,
				state.primary < min || state.primary > max ? red : green
			);
			label(context, `10^${state.primary.toFixed(1)}`, rangeStart, y + 30, '#a1a1aa');
		});
		return;
	}
	if (id.includes('loss-scaling')) {
		const gradients = [1e-8, 3e-8, 7e-8, 2e-7];
		const baseline = 6e-8;
		label(context, `FP16 underflow threshold ≈ ${baseline.toExponential(0)}`, pad, 28);
		['raw gradient', 'after loss scale', 'after unscale'].forEach((name, row) => {
			const y = 58 + row * 70;
			label(context, name, pad, y + 14);
			gradients.forEach((gradient, index) => {
				const shown = row === 1 && state.mode === 'on' ? gradient * state.primary : gradient;
				const survives =
					row === 1 && state.mode === 'on' ? shown >= baseline : gradient >= baseline;
				box(
					context,
					pad + 130 + index * 62,
					y,
					42,
					28,
					survives || (row === 2 && state.mode === 'on') ? green : red
				);
				label(
					context,
					row === 1 ? (survives ? 'kept' : 'zero') : gradient.toExponential(0),
					pad + 131 + index * 62,
					y + 43
				);
			});
		});
		return;
	}
	if (id.includes('magnitude-pruning') || id.includes('iterative-pruning')) {
		const columns = 10;
		const rows = 6;
		const sparsity = Math.round(state.primary);
		const prunedCount = Math.round((rows * columns * sparsity) / 100);
		label(context, `Weight matrix · ${sparsity}% target sparsity`, pad, 28);
		for (let index = 0; index < rows * columns; index++) {
			const column = index % columns;
			const row = Math.floor(index / columns);
			const pruned = index < prunedCount;
			box(
				context,
				pad + column * ((width - pad * 2) / columns),
				55 + row * 34,
				(width - pad * 2) / columns - 4,
				26,
				pruned ? '#3f3f46' : [blue, accent, green, orange][index % 4]
			);
		}
		label(
			context,
			`${prunedCount} pruned · ${rows * columns - prunedCount} retained`,
			pad,
			height - 25,
			green
		);
		if (id.includes('iterative-pruning') && state.mode === 'iterative') {
			const rounds = Math.max(1, Math.round(state.secondary));
			const rampY = height - 78;
			for (let round = 0; round < rounds; round++) {
				const rampWidth = (width - pad * 2) / rounds;
				box(context, pad + round * rampWidth, rampY, rampWidth - 3, 12 + (round + 1) * 4, accent);
			}
			label(
				context,
				`iterative schedule · ${rounds} prune / fine-tune rounds`,
				pad,
				rampY - 9,
				orange
			);
		}
		return;
	}
	if (id.includes('kernel-fusion')) {
		const barWidth = width * 0.28;
		const multiplier = state.mode === 'fused' ? 2 : 4;
		label(context, 'Estimated memory traffic for two elementwise ops', pad, 28);
		[
			{ name: 'unfused passes', value: 4, color: orange },
			{ name: 'fused pass', value: multiplier, color: green }
		].forEach(({ name, value, color }, index) => {
			const x = width * (index === 0 ? 0.2 : 0.62);
			box(context, x, height - 75, barWidth * (value / 4), 34, color);
			label(context, `${name} · ${value} array transfers`, x, height - 28, color);
		});
		return;
	}
	if (id.includes('real-kernels-cuda-triton')) {
		const threads = Math.max(1, Math.round(state.secondary));
		const blocks = Math.ceil(state.primary / threads);
		label(context, `Grid: ${blocks} blocks × ${threads} threads`, pad, 28);
		for (let blockIndex = 0; blockIndex < Math.min(blocks, 6); blockIndex++) {
			const x = pad + blockIndex * ((width - pad * 2) / Math.min(blocks, 6));
			const blockWidth = (width - pad * 2) / Math.min(blocks, 6) - 5;
			box(context, x, 70, blockWidth, 90, '#27272a');
			label(context, `block ${blockIndex}`, x + 3, 58, blue);
			for (let thread = 0; thread < Math.min(threads, 12); thread++) {
				box(
					context,
					x + 4 + thread * ((blockWidth - 8) / Math.min(threads, 12)),
					82,
					(blockWidth - 10) / Math.min(threads, 12),
					52,
					green
				);
			}
		}
		label(
			context,
			`${blocks * threads - state.primary} idle threads in final block`,
			pad,
			height - 28,
			orange
		);
		return;
	}
	if (id.includes('torch-compile-graph-compilation')) {
		const operations = Math.max(2, Math.min(12, Math.round(state.primary / 8)));
		const compiled = state.mode === 'compiled';
		const events = compiled
			? [
					{
						label: `${operations} fused ops`,
						start: 0,
						duration: operations,
						lane: 0,
						color: green
					}
				]
			: Array.from({ length: operations }, (_, index) => ({
					label: `op ${index + 1}`,
					start: index * 1.2,
					duration: 0.8,
					lane: 0,
					color: blue
				}));
		label(
			context,
			compiled ? 'Compiled graph · fused dispatch' : 'Eager execution · per-op dispatch',
			pad,
			28
		);
		drawTimeline(context, {
			x: pad,
			y: 75,
			width: width - pad * 2,
			height: 90,
			duration: operations * 1.2,
			lanes: ['GPU work'],
			events
		});
		return;
	}
	if (id.includes('torchscript-onnx-export')) {
		const exported = state.mode === 'exported';
		const y = 74;
		label(context, 'Python eager stack', pad, 38, orange);
		label(context, 'Exported runtime', width / 2 + 12, 38, green);
		for (let index = 0; index < 4; index++) {
			box(context, pad + index * 72, y, 64, 42, exported ? '#27272a' : orange);
		}
		for (let index = 0; index < 2; index++) {
			box(context, width / 2 + 12 + index * 100, y, 90, 42, exported ? green : '#27272a');
		}
		label(
			context,
			exported ? 'Portable graph selected' : 'Export the graph to reduce serving dependencies',
			pad,
			150
		);
		return;
	}

	const bars = Math.max(4, Math.min(12, Math.round(state.n / 6)));
	const max = Math.max(...state.samples, 1);
	for (let index = 0; index < bars; index++) {
		const value = state.samples[index] ?? 0.1 + random() * 0.9;
		const x = pad + index * ((width - pad * 2) / bars);
		const barHeight = Math.max(8, (height - 90) * (value / max));
		box(
			context,
			x,
			height - 44 - barHeight,
			(width - pad * 2) / bars - 5,
			barHeight,
			index === Math.round(state.step) % bars ? accent : blue
		);
		label(context, `${index + 1}`, x + 2, height - 26, '#a1a1aa');
	}
	label(context, id.replace('systems-perf-', '').replaceAll('-', ' '), pad, 25);
}

/**
 * @param {string} id
 * @param {State} state
 * @returns {Array<{ label: string; value: string | number }>}
 */
function getStatsRows(id, state) {
	if (id === 'inf-attn-scaled-dot-product') {
		const dimension = Math.max(1, state.secondary);
		const scale = state.mode === 'unscaled' ? 1 : Math.sqrt(dimension);
		const tokenCount = Math.max(2, state.primary);
		return [
			{ label: 'head dimension dₖ', value: Math.round(dimension) },
			{ label: 'score range (illustrative)', value: `±${(Math.sqrt(dimension) * 2).toFixed(1)}` },
			{ label: 'scaled score range', value: `±${((Math.sqrt(dimension) * 2) / scale).toFixed(1)}` },
			{ label: 'row entropy upper bound', value: `${Math.log2(tokenCount).toFixed(2)} bits` }
		];
	}
	if (id === 'inf-attn-multi-head') {
		const dimensions = state.primary * state.secondary;
		return [
			{
				label: 'heads × head dim',
				value: `${Math.round(state.primary)} × ${Math.round(state.secondary)}`
			},
			{ label: 'embedding dimension', value: Math.round(dimensions) },
			{ label: 'output projection params', value: Math.round(dimensions ** 2).toLocaleString() }
		];
	}
	if (id.startsWith('inf-attn-')) {
		const heads = Math.max(1, state.primary);
		const groups = id === 'inf-attn-multi-query' ? 1 : Math.min(heads, state.secondary);
		const dim = id === 'inf-attn-multi-head-latent' ? state.secondary : 4;
		const mhaElements = state.n * heads * dim * 2;
		const variantElements = state.n * groups * dim * 2;
		return [
			{ label: 'MHA KV elements / token', value: heads * dim * 2 },
			{ label: 'current KV elements', value: variantElements.toLocaleString() },
			{ label: 'cache reduction vs MHA', value: `${(mhaElements / variantElements).toFixed(1)}×` }
		];
	}
	if (id === 'inf-kv-rope-decoding') {
		const thetaM = state.primary * 0.07;
		const thetaN = (state.primary + state.secondary) * 0.07;
		return [
			{ label: 'θₘ', value: `${thetaM.toFixed(3)} rad` },
			{ label: 'θₙ', value: `${thetaN.toFixed(3)} rad` },
			{ label: 'relative angle / dot product', value: `${(thetaN - thetaM).toFixed(3)} rad` }
		];
	}
	if (id === 'inf-kv-autoregressive-cache') {
		const prompt = state.primary;
		const steps = state.secondary;
		const cachedWork = prompt * steps + (steps * (steps + 1)) / 2;
		const uncachedWork = Array.from(
			{ length: steps },
			(_, index) => (prompt + index + 1) ** 2
		).reduce((sum, value) => sum + value, 0);
		return [
			{ label: 'cached attention work (relative)', value: Math.round(cachedWork).toLocaleString() },
			{ label: 'recomputed work (relative)', value: Math.round(uncachedWork).toLocaleString() },
			{ label: 'estimated work reduction', value: `${(uncachedWork / cachedWork).toFixed(1)}×` }
		];
	}
	if (id === 'inf-kv-memory-footprint') {
		const perToken = state.primary * state.secondary * state.n * 2;
		return [
			{ label: 'MHA cache (Ki elements)', value: ((perToken * 12) / 1024).toFixed(1) },
			{ label: 'GQA cache (Ki elements)', value: ((perToken * 4) / 1024).toFixed(1) },
			{ label: 'MQA cache (Ki elements)', value: ((perToken * 1) / 1024).toFixed(1) }
		];
	}
	if (id === 'inf-kv-paged-attention') {
		const total = Math.max(8, Math.min(30, Math.round(state.n / 4)));
		const used = Math.min(total, Math.round(state.step));
		return [
			{ label: 'physical blocks', value: total },
			{ label: 'allocated / free', value: `${used} / ${total - used}` },
			{ label: 'pool utilization', value: `${Math.round((used / total) * 100)}%` }
		];
	}
	if (id === 'inf-kv-prefix-cache') {
		const requestLength = Math.max(1, state.primary);
		const sharedLength = Math.min(requestLength, state.secondary);
		return [
			{ label: 'shared prefix reused', value: `${Math.round(sharedLength)} tokens` },
			{
				label: 'new suffix to compute',
				value: `${Math.round(requestLength - sharedLength)} tokens`
			},
			{ label: 'tokens saved', value: `${((sharedLength / requestLength) * 100).toFixed(0)}%` }
		];
	}
	if (id.includes('roofline')) {
		const intensity = state.primary * state.secondary;
		return [
			{ label: 'arithmetic intensity (illustrative)', value: `${intensity.toFixed(1)} FLOPs/byte` },
			{ label: 'operating regime', value: intensity > 80 ? 'compute-bound' : 'memory-bound' },
			{ label: 'batch size', value: Math.round(state.primary) }
		];
	}
	if (id.includes('quantize') || id.includes('dequantize') || id.includes('inf-quant-')) {
		const scale = state.secondary / 127;
		return [
			{ label: 'scale factor', value: scale.toFixed(4) },
			{ label: 'estimated mean abs. error', value: (scale / 4).toFixed(4) },
			{
				label: 'quantization format',
				value: id.includes('int4') ? 'INT4' : id.includes('fp8') ? 'FP8' : 'INT8'
			}
		];
	}
	if (id.startsWith('inf-batch-')) {
		if (id.includes('latency-percentiles')) {
			return [
				{ label: 'P50 latency (relative)', value: `${Math.round(state.primary)} ms` },
				{
					label: 'P95 latency (relative)',
					value: `${Math.round(state.primary * (1 + state.secondary / 10))} ms`
				},
				{
					label: 'P99 latency (relative)',
					value: `${Math.round(state.primary * (1 + state.secondary / 5))} ms`
				}
			];
		}
		if (id.includes('serving-metrics')) {
			return [
				{ label: 'TTFT (relative)', value: `${Math.round(state.primary * 2)} ms` },
				{ label: 'TPOT / mean ITL', value: `${state.secondary} ms/token` },
				{
					label: 'output throughput',
					value: `${(1000 / Math.max(1, state.secondary)).toFixed(1)} tokens/s`
				}
			];
		}
		if (id.includes('dynamic-request-batching')) {
			return [
				{ label: 'max batch wait', value: `${Math.round(state.primary)} ms` },
				{ label: 'batch capacity', value: Math.round(state.secondary) },
				{
					label: 'estimated slot utilization',
					value: `${Math.min(99, Math.round(35 + state.secondary * 3))}%`
				}
			];
		}
		if (id.includes('continuous-batching')) {
			return [
				{ label: 'batch slots', value: Math.round(state.primary) },
				{ label: 'static slots freed early', value: Math.max(0, Math.round(state.primary / 2)) },
				{ label: 'decode iteration', value: Math.round(state.step) }
			];
		}
		if (id.includes('chunked-prefill')) {
			return [
				{ label: 'prompt tokens', value: Math.round(state.primary) },
				{ label: 'prefill chunk size', value: Math.round(state.secondary) },
				{ label: 'decode requests', value: Math.round(state.n) }
			];
		}
		return [
			{ label: 'configured requests', value: Math.round(state.n) },
			{ label: 'step / batch-window setting', value: Math.round(state.secondary) },
			{ label: 'timeline steps advanced', value: Math.round(state.step) }
		];
	}
	if (id === 'systems-perf-quantize-float32-to-int8') {
		const scale = Math.max(0.001, state.secondary / 127);
		const quantized = Math.max(-128, Math.min(127, Math.round(state.primary / scale)));
		const reconstructed = quantized * scale;
		return [
			{ label: 'input float x', value: state.primary.toFixed(2) },
			{ label: 'quantized integer q', value: quantized },
			{
				label: 'reconstructed value · abs error',
				value: `${reconstructed.toFixed(2)} · ${Math.abs(reconstructed - state.primary).toFixed(3)}`
			}
		];
	}
	if (id === 'systems-perf-dequantize-int8-to-float32') {
		return [
			{ label: 'quantized integer q', value: Math.round(state.primary) },
			{ label: 'scale', value: (state.secondary / 127).toFixed(4) },
			{ label: 'reconstructed float', value: ((state.primary * state.secondary) / 127).toFixed(3) }
		];
	}
	if (id === 'systems-perf-quantize-weight-matrix-tradeoff') {
		const rows = Math.round(state.primary);
		const columns = Math.round(state.secondary);
		return [
			{ label: 'matrix shape', value: `${rows} × ${columns}` },
			{
				label: 'FP32 → INT8 storage',
				value: `${((rows * columns * 4) / 1024).toFixed(1)} → ${((rows * columns) / 1024).toFixed(1)} KiB`
			},
			{ label: 'storage reduction', value: '75% · 4× smaller' }
		];
	}
	if (id.includes('checkpoint')) {
		const interval = Math.max(1, Math.round(state.secondary));
		return [
			{ label: 'training steps', value: Math.round(state.primary) },
			{ label: 'checkpoint every', value: `${interval} steps` },
			{ label: 'steps lost on crash', value: Math.round(state.step) % interval }
		];
	}
	if (id.includes('timing')) {
		const durations = state.samples.slice(-12);
		const mean = durations.reduce((sum, duration) => sum + duration, 0) / durations.length;
		return [
			{ label: 'measured calls', value: durations.length },
			{ label: 'latest duration', value: `${durations.at(-1)?.toFixed(3) ?? '—'} ms` },
			{
				label: 'mean / min',
				value: durations.length
					? `${mean.toFixed(3)} / ${Math.min(...durations).toFixed(3)} ms`
					: '—'
			}
		];
	}
	if (id.includes('vectorize')) {
		return [
			{ label: 'naive loop', value: `${state.samples[0]?.toFixed(3) ?? '—'} ms` },
			{ label: 'NumPy vectorized', value: `${state.samples[1]?.toFixed(3) ?? '—'} ms` },
			{
				label: 'measured speedup',
				value: state.samples[1] > 0 ? `${(state.samples[0] / state.samples[1]).toFixed(2)}×` : '—'
			}
		];
	}
	if (id.includes('parameter')) {
		const layerCount = Math.round(state.secondary);
		const perLayer = Math.round(state.primary ** 2);
		return [
			{ label: 'linear weights / layer', value: perLayer.toLocaleString() },
			{ label: 'linear stack total', value: (perLayer * layerCount).toLocaleString() },
			{ label: 'layers in stack', value: layerCount }
		];
	}
	if (id.includes('flops')) {
		const params = state.primary * state.secondary;
		return [
			{ label: 'linear parameters', value: Math.round(params).toLocaleString() },
			{ label: 'forward FLOPs estimate', value: Math.round(2 * params * state.n).toLocaleString() },
			{ label: 'FLOPs / parameter', value: Math.round(2 * state.n) }
		];
	}
	if (id.includes('memory')) {
		const parameterGb = (state.primary * 1_000_000 * state.secondary) / 1_000_000_000;
		return [
			{ label: 'parameter storage (selected precision)', value: `${parameterGb.toFixed(2)} GB` },
			{
				label: 'training estimate (Adam + activations)',
				value: `${(parameterGb * 4 + state.n * 0.1).toFixed(2)} GB`
			},
			{ label: 'batch size', value: Math.round(state.n) }
		];
	}
	if (id === 'systems-perf-kernel-fusion') {
		const elements = state.primary * 1_000;
		const unfusedBytes = elements * state.secondary * 4;
		return [
			{
				label: 'unfused traffic (2 reads + 2 writes)',
				value: `${((unfusedBytes * 4) / 1_000_000).toFixed(2)} MB`
			},
			{
				label: 'fused traffic (1 read + 1 write)',
				value: `${((unfusedBytes * 2) / 1_000_000).toFixed(2)} MB`
			},
			{ label: 'traffic reduction', value: '50% · one fewer round-trip' }
		];
	}
	if (id === 'systems-perf-real-kernels-cuda-triton') {
		const problemSize = Math.round(state.primary);
		const threads = Math.max(1, Math.round(state.secondary));
		const blocks = Math.ceil(problemSize / threads);
		return [
			{ label: 'problem elements', value: problemSize },
			{ label: 'blocks × threads / block', value: `${blocks} × ${threads}` },
			{ label: 'wasted threads in last block', value: blocks * threads - problemSize }
		];
	}
	if (id === 'systems-perf-torch-compile-graph-compilation') {
		const operations = Math.round(state.primary);
		const overhead = state.secondary;
		return [
			{ label: 'graph operations', value: operations },
			{
				label: 'eager dispatch overhead estimate',
				value: `${(operations * overhead).toFixed(1)} μs`
			},
			{ label: 'compiled dispatches', value: state.mode === 'compiled' ? 1 : operations }
		];
	}
	if (id === 'systems-perf-torchscript-onnx-export') {
		return [
			{ label: 'Python eager layers', value: 'Python + PyTorch + GIL' },
			{ label: 'exported serving layers', value: 'Graph + runtime' },
			{
				label: 'overhead comparison',
				value: state.mode === 'exported' ? 'fewer runtime layers' : 'full Python stack'
			}
		];
	}
	if (id.includes('loss-scaling')) {
		return [
			{ label: 'loss scale factor', value: Math.round(state.primary) },
			{ label: 'gradient before scale', value: (1e-8 * state.secondary).toExponential(2) },
			{ label: 'after scale then unscale', value: (1e-8 * state.secondary).toExponential(2) }
		];
	}
	if (id.includes('fp16-bf16')) {
		const exponent = state.primary;
		return [
			{ label: 'illustrative value', value: `10^${exponent.toFixed(1)}` },
			{
				label: 'FP16 range status',
				value: exponent < -7 ? 'underflow risk' : exponent > 4.8 ? 'overflow' : 'representable'
			},
			{
				label: 'BF16 / FP32 range status',
				value: exponent > 38 ? 'overflow risk' : 'representable'
			}
		];
	}
	if (id.includes('loss-scaling')) {
		const tinyGradients = [1e-8, 3e-8, 7e-8, 2e-7];
		const underflowWithout = tinyGradients.filter((gradient) => gradient < 6e-8).length;
		const scale = Math.max(1, state.primary);
		const survivingWith = tinyGradients.filter((gradient) => gradient * scale >= 6e-8).length;
		return [
			{ label: 'scale factor', value: `×${Math.round(scale)}` },
			{ label: 'FP16 gradients underflowed without scaling', value: underflowWithout },
			{ label: 'survive scale → unscale', value: `${survivingWith} / ${tinyGradients.length}` }
		];
	}
	if (id.includes('autocast')) {
		return [
			{
				label: 'reduced precision ops',
				value: state.mode === 'off' ? 0 : Math.round(state.primary * 0.6)
			},
			{ label: 'FP32-sensitive ops', value: Math.round(state.primary * 0.4) },
			{
				label: 'precision policy',
				value: state.mode === 'off' ? 'FP32 only' : 'selective autocast'
			}
		];
	}
	if (id.includes('pruning')) {
		return [
			{ label: 'target sparsity', value: `${Math.round(state.primary)}%` },
			{
				label: 'weights removed (estimate)',
				value: Math.round(state.primary * state.secondary).toLocaleString()
			},
			{ label: 'pruning rounds', value: Math.round(state.secondary) }
		];
	}
	if (id.includes('distillation')) {
		return [
			{ label: 'temperature', value: state.primary.toFixed(1) },
			{ label: 'student confidence', value: `${Math.round(state.secondary)}%` },
			{
				label: 'KL divergence (illustrative)',
				value: (1 / Math.max(0.1, state.primary)).toFixed(3)
			}
		];
	}
	return [
		{ label: 'configured work size', value: Math.round(state.primary) },
		{ label: 'configured parameter', value: Math.round(state.secondary) },
		{ label: 'current step', value: Math.round(state.step) }
	];
}

/** @param {HTMLElement} root */
export function mount(root) {
	const id = root.dataset.widget ?? '';
	if (!systemsVisualizerIdSet.has(id)) return () => {};
	const hash = Array.from(id).reduce(
		(sum, character) => (sum * 31 + character.charCodeAt(0)) >>> 0,
		7
	);
	const random = seededRandom(hash);
	/** @type {State} */
	const state = {
		primary: 4,
		secondary: 2,
		n: 64,
		step: 0,
		mode: 'on',
		samples:
			id.includes('timing') || id.includes('vectorize')
				? []
				: Array.from({ length: 12 }, () => 0.2 + random()),
		blocks: [],
		events: [],
		running: false,
		result: ''
	};
	/** @type {Array<() => void>} */
	const listeners = [];
	const shell = document.createElement('section');
	shell.className = 'tt-widget tt-systems-viz';
	const heading = document.createElement('h4');
	heading.textContent = 'Try it live';
	const stage = document.createElement('div');
	stage.className = 'viz-stage';
	const controls = document.createElement('div');
	controls.className = 'viz-controls controls';
	const stats = createStatsPanel();
	const buttons = document.createElement('div');
	buttons.className = 'btnrow';
	const benchmarkStatus = document.createElement('p');
	benchmarkStatus.className = 'viz-status';
	benchmarkStatus.setAttribute('role', 'status');
	benchmarkStatus.setAttribute('aria-live', 'polite');
	const caption = document.createElement('p');
	caption.className = 'viz-caption';
	caption.textContent =
		captions[id] ?? 'Explore this system concept with the interactive controls.';
	let plot = createCanvasPlot((context, width, height) =>
		draw(id, state, width, height, context, hash)
	);
	stage.append(plot.element);

	/** @type {Record<string, string[]>} */
	const sliderLabels = {
		'inf-attn-scaled-dot-product': ['Token count', 'Head dimension'],
		'inf-attn-multi-head': ['Number of heads', 'Head dimension', 'Token count'],
		'inf-attn-multi-query': ['Query heads', 'Head dimension', 'Sequence length'],
		'inf-attn-grouped-query': ['Query heads', 'KV groups', 'Sequence length'],
		'inf-attn-multi-head-latent': ['Query heads', 'Latent dimension', 'Sequence length'],
		'inf-kv-rope-decoding': ['Position m', 'Relative offset'],
		'inf-kv-autoregressive-cache': ['Prompt length (tokens)', 'Decode steps'],
		'inf-kv-memory-footprint': ['Sequence length', 'Batch size', 'Transformer layers'],
		'inf-kv-paged-attention': ['Physical block count', 'Tokens per block'],
		'inf-kv-prefix-cache': ['Request length (tokens)', 'Shared prefix length'],
		'inf-quant-int8-symmetric': ['Value distribution range', 'Quantization scale'],
		'inf-quant-per-channel': ['Row magnitude spread', 'Weight rows', 'Weight columns'],
		'inf-quant-int4-groupwise': ['Group size (weights)', 'Quantization range'],
		'inf-quant-fp8-blockwise': ['Block size (values)', 'Distribution tail weight'],
		'inf-quant-roofline': ['Decode batch size', 'Prompt sequence length'],
		'inf-batch-latency-percentiles': ['Request samples', 'Slow-tail fraction'],
		'inf-batch-serving-metrics-ttft-tpot-itl': [
			'Prompt length (tokens)',
			'Output tokens',
			'Decode time (ms)'
		],
		'inf-batch-dynamic-request-batching': [
			'Batch window (ms)',
			'Maximum batch size',
			'Incoming requests'
		],
		'inf-batch-continuous-batching': ['Batch slots', 'Decode steps', 'Requests'],
		'inf-batch-chunked-prefill': [
			'Prompt length (tokens)',
			'Prefill chunk size',
			'Active decode requests'
		],
		'systems-perf-timing-decorator': ['Work per call (×1k)', 'Warm-up work'],
		'systems-perf-parameter-counting': ['Layer width', 'Layer count', 'Vocabulary size'],
		'systems-perf-memory-footprint-estimation': [
			'Parameters (millions)',
			'Bytes per parameter',
			'Batch size'
		],
		'systems-perf-flops-estimation': ['Input features', 'Output features', 'Batch size'],
		'systems-perf-checkpointing': ['Training steps', 'Checkpoint interval', 'Steps run'],
		'systems-perf-quantize-float32-to-int8': ['Float value x', 'Quantization scale'],
		'systems-perf-dequantize-int8-to-float32': ['Quantized integer q', 'Quantization scale'],
		'systems-perf-quantize-weight-matrix-tradeoff': [
			'Matrix rows',
			'Matrix columns',
			'Scale granularity'
		],
		'systems-perf-fp16-bf16-representable-range': ['Log₁₀(|value|)', 'Value sign'],
		'systems-perf-loss-scaling': ['Loss scale factor', 'Gradient magnitude'],
		'systems-perf-autocast-concept': ['Operations in graph', 'Reduced precision fraction'],
		'systems-perf-magnitude-pruning': [
			'Sparsity target (%)',
			'Weight distribution',
			'Matrix width'
		],
		'systems-perf-iterative-pruning-schedule': [
			'Target sparsity (%)',
			'Pruning rounds',
			'Training steps'
		],
		'systems-perf-knowledge-distillation': ['Temperature', 'Student confidence'],
		'systems-perf-vectorize-naive-loop': ['Array size (×500)', 'Work per element'],
		'systems-perf-kernel-fusion': ['Array size (×1k)', 'Bytes per element'],
		'systems-perf-roofline-model': ['Arithmetic intensity', 'Memory bandwidth'],
		'systems-perf-real-kernels-cuda-triton': ['Problem size', 'Threads per block', 'Block count'],
		'systems-perf-torch-compile-graph-compilation': ['Operation count', 'Dispatch overhead (μs)'],
		'systems-perf-torchscript-onnx-export': ['Model operations', 'Exported operations']
	};
	const labels = sliderLabels[id] ?? ['Work items', 'Parameter value'];
	const isAttention = id.startsWith('inf-attn-');
	/** @type {Record<string, [number, number, number, number]>} */
	const primaryRanges = {
		'inf-attn-scaled-dot-product': [2, 6, 1, 4],
		'systems-perf-knowledge-distillation': [0.5, 5, 0.5, 1],
		'systems-perf-fp16-bf16-representable-range': [-10, 10, 0.1, -4],
		'systems-perf-quantize-float32-to-int8': [-10, 10, 0.1, 2],
		'systems-perf-dequantize-int8-to-float32': [-128, 127, 1, 24],
		'systems-perf-loss-scaling': [1, 1024, 1, 128],
		'systems-perf-magnitude-pruning': [0, 90, 1, 50],
		'systems-perf-iterative-pruning-schedule': [10, 90, 1, 60]
	};
	const primaryRange = primaryRanges[id] ?? [1, 128, 1, isAttention ? 4 : 64];
	const primarySettings = {
		label: labels[0],
		min: primaryRange[0],
		max: primaryRange[1],
		step: primaryRange[2],
		value: primaryRange[3]
	};
	const secondarySettings = {
		label: labels[1],
		min: 1,
		max: 16,
		step: 1,
		value: id === 'inf-attn-grouped-query' ? 2 : 4
	};
	const nSettings = labels[2]
		? {
				label: labels[2],
				min: 1,
				max: id === 'inf-attn-multi-head' ? 6 : 128,
				step: id === 'inf-attn-multi-head' ? 1 : 8,
				value: id === 'inf-attn-multi-head' ? 4 : 64
			}
		: undefined;
	state.primary = primarySettings.value;
	state.secondary = secondarySettings.value;
	state.n = nSettings?.value ?? state.n;
	const settings = { primary: primarySettings, secondary: secondarySettings, n: nSettings };
	/** @type {Partial<Record<'primary' | 'secondary' | 'n', ReturnType<typeof createSlider>>>} */
	const sliders = {};
	for (const key of /** @type {const} */ (['primary', 'secondary', 'n'])) {
		if (key === 'n' && !nSettings) continue;
		const currentSettings = settings[key];
		if (!currentSettings) continue;
		const slider = createSlider(currentSettings);
		sliders[key] = slider;
		controls.append(slider.element);
		const onInput = () => {
			state[key] = Number(slider.input.value);
			update();
		};
		slider.input.addEventListener('input', onInput);
		listeners.push(() => slider.input.removeEventListener('input', onInput));
	}

	const modeSelect = document.createElement('select');
	modeSelect.className = 'viz-select';
	/** @type {Record<string, { label: string; options: Array<[string, string]> }>} */
	const modeOptions = {
		'inf-attn-scaled-dot-product': {
			label: 'Attention score scaling',
			options: [
				['scaled', 'Scale by √d'],
				['unscaled', 'No scaling']
			]
		},
		'inf-kv-paged-attention': {
			label: 'KV allocation strategy',
			options: [
				['on', 'Paged allocation'],
				['naive', 'Naive contiguous']
			]
		},
		'inf-kv-autoregressive-cache': {
			label: 'Generation cache mode',
			options: [
				['on', 'With cache'],
				['recompute', 'Recompute']
			]
		},
		'inf-batch-continuous-batching': {
			label: 'Batching strategy',
			options: [
				['static', 'Static batching'],
				['continuous', 'Continuous batching']
			]
		},
		'inf-batch-chunked-prefill': {
			label: 'Prefill scheduling',
			options: [
				['unchunked', 'Unchunked prefill'],
				['chunked', 'Chunked prefill']
			]
		},
		'inf-batch-dynamic-request-batching': {
			label: 'Request dispatch mode',
			options: [
				['windowed', 'Windowed batching'],
				['immediate', 'Dispatch immediately']
			]
		},
		'inf-quant-per-channel': {
			label: 'Weight scaling granularity',
			options: [
				['tensor', 'Per tensor'],
				['channel', 'Per channel']
			]
		},
		'inf-quant-fp8-blockwise': {
			label: 'Quantization format',
			options: [
				['int8', 'INT8 grid'],
				['fp8', 'FP8 E4M3 grid']
			]
		},
		'systems-perf-quantize-weight-matrix-tradeoff': {
			label: 'Weight scaling granularity',
			options: [
				['tensor', 'Per tensor'],
				['channel', 'Per channel']
			]
		},
		'systems-perf-magnitude-pruning': {
			label: 'Weight distribution',
			options: [
				['normal', 'Normal weights'],
				['outliers', 'Weights with outliers']
			]
		},
		'systems-perf-timing-decorator': {
			label: 'Warm-up call',
			options: [
				['off', 'Skip warm-up'],
				['on', 'Include warm-up']
			]
		},
		'systems-perf-loss-scaling': {
			label: 'Loss scaling',
			options: [
				['on', 'With loss scaling'],
				['off', 'Without loss scaling']
			]
		},
		'systems-perf-autocast-concept': {
			label: 'Autocast',
			options: [
				['on', 'Autocast enabled'],
				['off', 'Autocast disabled']
			]
		},
		'systems-perf-iterative-pruning-schedule': {
			label: 'Pruning schedule',
			options: [
				['one-shot', 'One-shot pruning'],
				['iterative', 'Iterative pruning']
			]
		},
		'systems-perf-kernel-fusion': {
			label: 'Kernel execution',
			options: [
				['unfused', 'Two unfused passes'],
				['fused', 'One fused pass']
			]
		},
		'systems-perf-roofline-model': {
			label: 'Elementwise fusion',
			options: [
				['off', 'Unfused elementwise op'],
				['on', 'Fused elementwise op']
			]
		},
		'systems-perf-torch-compile-graph-compilation': {
			label: 'Execution mode',
			options: [
				['eager', 'Eager execution'],
				['compiled', 'Compiled graph']
			]
		},
		'systems-perf-torchscript-onnx-export': {
			label: 'Deployment format',
			options: [
				['python', 'Python eager serving'],
				['exported', 'Exported graph serving']
			]
		}
	};
	const modes =
		modeOptions[id]?.options ??
		([
			'inf-quant-int8-symmetric',
			'systems-perf-quantize-float32-to-int8',
			'systems-perf-dequantize-int8-to-float32'
		].includes(id)
			? [
					['on', 'Auto scale'],
					['manual', 'Manual scale']
				]
			: []);
	state.mode = modes[0]?.[0] ?? 'on';
	if (modes.length > 0) {
		modeSelect.setAttribute('aria-label', modeOptions[id]?.label ?? 'Quantization scale mode');
		for (const [value, text] of modes) {
			const option = document.createElement('option');
			option.value = value;
			option.textContent = text;
			modeSelect.append(option);
		}
		const onModeChange = () => {
			state.mode = modeSelect.value;
			update();
		};
		modeSelect.addEventListener('change', onModeChange);
		listeners.push(() => modeSelect.removeEventListener('change', onModeChange));
		controls.prepend(modeSelect);
	}

	const update = () => {
		plot.destroy();
		plot = createCanvasPlot((context, width, height) =>
			draw(id, state, width, height, context, hash)
		);
		stage.replaceChildren(plot.element);
		stats.update(getStatsRows(id, state));
	};
	/**
	 * @param {string} text
	 * @param {() => void} action
	 * @param {boolean} [primary]
	 */
	const addButton = (text, action, primary = false) => {
		const button = createActionButton(text, { primary });
		button.addEventListener('click', action);
		listeners.push(() => button.removeEventListener('click', action));
		buttons.append(button);
		return button;
	};
	/** @type {HTMLButtonElement | undefined} */
	let runButton;
	let disposed = false;
	const realBenchmark = id.includes('timing') || id.includes('vectorize');
	const onStep = async () => {
		if (realBenchmark) {
			if (state.running) return;
			state.running = true;
			if (runButton) runButton.disabled = true;
			benchmarkStatus.textContent = 'Starting Pyodide and preparing the Python benchmark…';
			const workSize = Math.round(state.primary * (id.includes('timing') ? 2_000 : 500));
			const source = id.includes('timing')
				? `
import math, time
work = ${workSize}
def timed_work():
    total = 0.0
    for index in range(work):
        total += math.sqrt(index + 1)
    return total
if ${state.mode === 'on' ? 'True' : 'False'}:
    timed_work()
start = time.perf_counter()
first_result = timed_work()
first_ms = (time.perf_counter() - start) * 1000
start = time.perf_counter()
second_result = timed_work()
second_ms = (time.perf_counter() - start) * 1000
`
				: `
import time
import numpy as np
values = np.linspace(0.0, 1.0, ${workSize}, dtype=np.float64)
start = time.perf_counter()
first_result = sum(float(value) * float(value) + 1.0 for value in values)
first_ms = (time.perf_counter() - start) * 1000
start = time.perf_counter()
second_result = float(np.sum(np.square(values) + 1.0))
second_ms = (time.perf_counter() - start) * 1000
`;
			try {
				const result = await runPythonBenchmark(source, id.includes('vectorize') ? ['numpy'] : []);
				if (disposed) return;
				state.samples = id.includes('timing')
					? [...state.samples, result.firstMs, result.secondMs].slice(-12)
					: [result.firstMs, result.secondMs];
				state.step = state.samples.length;
				state.result = String(result.secondResult);
				benchmarkStatus.textContent =
					'Executed with Pyodide; all displayed timings are real measurements.';
				update();
			} catch (error) {
				if (!disposed) {
					benchmarkStatus.textContent = `Python benchmark failed: ${error instanceof Error ? error.message : String(error)}`;
				}
			} finally {
				state.running = false;
				if (runButton) runButton.disabled = false;
			}
			return;
		}
		state.step = state.step >= Math.min(12, Math.round(state.n / 4)) ? 0 : state.step + 1;
		update();
	};
	runButton = addButton(
		id.includes('timing') || id.includes('vectorize')
			? id.includes('timing')
				? 'Call function'
				: 'Run both implementations'
			: id.includes('checkpoint')
				? 'Advance step'
				: 'Step',
		onStep,
		true
	);
	if (id.includes('checkpoint') || id.includes('paged-attention') || id.includes('prefix-cache')) {
		addButton(id.includes('checkpoint') ? 'Simulate crash' : 'Add token', () => {
			state.step = Math.max(
				0,
				state.step - (id.includes('checkpoint') ? state.step % state.secondary : -1)
			);
			update();
		});
	}
	addButton('Reset', () => {
		state.primary = primarySettings.value;
		state.secondary = secondarySettings.value;
		state.n = nSettings?.value ?? 64;
		state.step = 0;
		state.mode = modes[0]?.[0] ?? 'on';
		state.samples =
			id.includes('timing') || id.includes('vectorize')
				? []
				: Array.from({ length: 12 }, () => 0.2 + random());
		if (modes.length > 0) modeSelect.selectedIndex = 0;
		for (const key of /** @type {const} */ (['primary', 'secondary', 'n'])) {
			const slider = sliders[key];
			if (!slider) continue;
			slider.input.value = String(state[key]);
			slider.update();
		}
		update();
	});

	shell.append(heading);
	const body = document.createElement('div');
	body.className = 'viz-stage';
	const layout = document.createElement('div');
	layout.className = 'viz-layout';
	layout.append(stage, controls);
	body.append(layout, buttons);
	if (realBenchmark) body.append(benchmarkStatus);
	body.append(stats.element);
	shell.append(body, caption);
	root.replaceChildren(shell);
	update();
	return () => {
		disposed = true;
		for (const cleanup of listeners) cleanup();
		plot.destroy();
		root.replaceChildren();
	};
}
