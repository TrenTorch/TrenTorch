import { describe, it, expect } from 'vitest';
import { readdirSync, readFileSync } from 'node:fs';
import { ALL_VIZ, initialState, type Control, type State, type VizConfig } from './index';

const SPECS = readdirSync('data/cuda/viz-specs')
	.filter((f) => f.startsWith('VIZ-'))
	.map((f) => f.slice(4, -3).toLowerCase());
/** specs that are extra modes of another figure rather than figures of their own */
const MODE_OF: Record<string, string> = {
	'occupancy-staircase': 'occupancy-calc',
	'roofline-ladder': 'roofline',
	'bank-stride-sweep': 'bank-grid'
};

const variants = (c: Control): (number | string | boolean)[] =>
	c.type === 'range'
		? [c.min, c.max, c.value, c.min + Math.round((c.max - c.min) / 2 / c.step) * c.step] // the slider only produces multiples of its step
		: c.type === 'select'
			? c.options.map((o) => o.value)
			: c.type === 'toggle'
				? [true, false]
				: ['T4', 'A100', 'H100'];

function check(c: VizConfig, state: State, mode?: string) {
	const out = c.compute(state, { mode });
	expect(out.live.length, `${c.id} has no aria-live sentence`).toBeGreaterThan(10);
	expect(out.live).not.toMatch(/NaN|undefined|\[object/);
	for (const p of out.panels) {
		if (p.kind === 'frames') {
			expect(p.frames.length).toBeGreaterThan(0);
			for (const f of p.frames) {
				expect(f.caption.length).toBeGreaterThan(0);
				for (const r of f.rows) expect(Array.isArray(r.cells)).toBe(true);
			}
		}
		if (p.kind === 'bars')
			for (const b of p.bars)
				for (const s of b.segments)
					expect(Number.isFinite(s.value), `${c.id}: bar ${b.label}`).toBe(true);
		if (p.kind === 'line')
			for (const s of p.series)
				for (const pt of s.points) {
					expect(
						Number.isFinite(pt[0]) && Number.isFinite(pt[1]),
						`${c.id}: ${s.name} point ${pt}`
					).toBe(true);
				}
	}
	for (const r of out.readouts)
		expect(r.value, `${c.id}: readout ${r.label}`).not.toMatch(/NaN|undefined/);
	return out;
}

describe('theory visualizations', () => {
	it('has one figure for every viz spec (extensions are modes of their parent)', () => {
		const have = new Set(ALL_VIZ.map((c) => c.id));
		const missing = SPECS.filter((s) => !have.has(s) && !have.has(MODE_OF[s]));
		expect(missing, `figures still to build: ${missing.join(', ')}`).toEqual([]);
		expect(new Set(ALL_VIZ.map((c) => c.id)).size).toBe(ALL_VIZ.length);
	});

	for (const c of ALL_VIZ) {
		it(`${c.id}: draws with its defaults and with every control at every setting`, () => {
			const base = initialState(c);
			check(c, base);
			for (const mode of Object.keys(c.modes ?? {})) check(c, initialState(c, mode), mode);
			for (const ctl of c.controls)
				for (const v of variants(ctl)) {
					check(c, { ...base, [ctl.id]: v });
					for (const mode of Object.keys(c.modes ?? {}))
						check(c, { ...initialState(c, mode), [ctl.id]: v }, mode);
				}
		});
	}

	it('uses the shared visual-language states and never relies on colour alone (cells carry text, a glyph or a pattern)', () => {
		const css = readFileSync('platform/components/cuda/viz/_shared/CellBox.svelte', 'utf8');
		for (const state of ['masked', 'stalled', 'error']) expect(css).toContain(state);
		expect(css).toContain('repeating-linear-gradient'); // masked = hatched
		expect(css).toContain('⏱'); // stalled = clock glyph
		expect(css).toContain('✕'); // error = cross glyph
	});
});
