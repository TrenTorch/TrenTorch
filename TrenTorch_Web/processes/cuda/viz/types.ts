// The shape of a theory visualization. A figure is a pure function from its control values to what to draw,
// computed with the model functions in processes/cuda/model. The Explorer component renders any config, so every
// figure gets the same visual language, a reduced-motion mode and an aria-live sentence for free.
import type { GpuName } from '../model/profiles';

export type CellState = 'idle' | 'active' | 'masked' | 'stalled' | 'touch' | 'error' | 'done';
export interface Cell {
	/** text inside the cell */
	text?: string;
	state?: CellState;
	/** 0 register .. 4 global: the five memory tints, warm to cool */
	tint?: 0 | 1 | 2 | 3 | 4;
	/** hover / screen-reader label */
	title?: string;
}
export interface Row {
	label: string;
	cells: Cell[];
	/** draw as a 32-lane strip */ lanes?: boolean;
	note?: string;
}
export interface Frame {
	rows: Row[];
	caption: string;
}

export type Tone =
	| 'memory'
	| 'compute'
	| 'launch'
	| 'good'
	| 'bad'
	| 'neutral'
	| 'tint0'
	| 'tint1'
	| 'tint2'
	| 'tint3'
	| 'tint4';
export interface BarSegment {
	value: number;
	tone: Tone;
	label?: string;
}
export interface Bar {
	label: string;
	segments: BarSegment[];
	note?: string;
}
export interface Series {
	name: string;
	tone: Tone;
	points: [number, number][];
	dashed?: boolean;
}

export type Panel =
	| { kind: 'frames'; title?: string; frames: Frame[] }
	| { kind: 'bars'; title?: string; unit?: string; max?: number; bars: Bar[] }
	| {
			kind: 'line';
			title?: string;
			xLabel: string;
			yLabel: string;
			xLog?: boolean;
			yLog?: boolean;
			yMax?: number;
			series: Series[];
			markers?: { x: number; label: string }[];
			point?: { x: number; y: number; label: string };
	  }
	| {
			kind: 'table';
			title?: string;
			header: string[];
			rows: (string | number)[][];
			highlight?: number;
	  }
	| { kind: 'text'; title?: string; text: string };

export interface Readout {
	label: string;
	value: string;
	hint?: string;
	tone?: 'good' | 'bad' | 'neutral';
}

export type Control =
	| {
			id: string;
			label: string;
			type: 'range';
			min: number;
			max: number;
			step: number;
			value: number;
			log?: boolean;
			format?: (v: number) => string;
			hint?: string;
	  }
	| {
			id: string;
			label: string;
			type: 'select';
			options: { value: string; label: string }[];
			value: string;
			hint?: string;
	  }
	| { id: string; label: string; type: 'toggle'; value: boolean; hint?: string }
	| { id: string; label: string; type: 'gpu'; value: GpuName; hint?: string };

export type State = Record<string, number | string | boolean>;
export interface VizOutput {
	panels: Panel[];
	readouts: Readout[];
	/** the aria-live sentence describing the current state */
	live: string;
	/** a short note shown under the figure, e.g. an "illustrative numbers" label */
	footnote?: string;
}
export interface VizConfig {
	id: string;
	title: string;
	controls: Control[];
	/** `mode` is set when a chapter embeds an extension of this figure (for example `staircase`) */
	compute: (state: State, ctx: { mode?: string; lastRun?: LastRun | null }) => VizOutput;
	/** controls to hide for a given mode */
	modes?: Record<string, { hide?: string[]; title?: string; presets?: State }>;
	/** shown when the figure's numbers are teaching numbers rather than hardware specs */
	illustrative?: boolean;
}

/** The learner's most recent simulator run, saved by the IDE (see cuda-service.ts); the roofline plots it. */
export interface LastRun {
	id: string;
	title: string;
	flops: number;
	bytes: number;
	gpu: string;
}
export const LAST_RUN_KEY = 'trentorch:cuda:lastrun';

export const initialState = (c: VizConfig, mode?: string): State => {
	const s: State = {};
	for (const ctl of c.controls) s[ctl.id] = ctl.value;
	return { ...s, ...(mode ? (c.modes?.[mode]?.presets ?? {}) : {}) };
};

// ---- small helpers shared by configs ----
export const num = (s: State, id: string) => Number(s[id]);
export const str = (s: State, id: string) => String(s[id]);
export const bool = (s: State, id: string) => Boolean(s[id]);
export const fmt = (x: number, digits = 3) =>
	Number.isFinite(x)
		? Number(x.toPrecision(digits)).toLocaleString('en-US', { maximumFractionDigits: 12 })
		: x > 0
			? 'infinite'
			: '-';
export const fmtTime = (seconds: number) =>
	seconds >= 1
		? `${fmt(seconds)} s`
		: seconds >= 1e-3
			? `${fmt(seconds * 1e3)} ms`
			: seconds >= 1e-6
				? `${fmt(seconds * 1e6)} us`
				: `${fmt(seconds * 1e9)} ns`;
export const fmtBytes = (b: number) =>
	b >= 1e9
		? `${fmt(b / 1e9)} GB`
		: b >= 1e6
			? `${fmt(b / 1e6)} MB`
			: b >= 1e3
				? `${fmt(b / 1e3)} KB`
				: `${fmt(b)} B`;
export const pct = (x: number) => `${fmt(x * 100, 3)}%`;
export const range = (
	id: string,
	label: string,
	min: number,
	max: number,
	step: number,
	value: number,
	extra: Partial<Extract<Control, { type: 'range' }>> = {}
): Control => ({ id, label, type: 'range', min, max, step, value, ...extra });
export const select = (
	id: string,
	label: string,
	options: [string, string][] | string[],
	value?: string
): Control => {
	const o = options.map((x) =>
		Array.isArray(x) ? { value: x[0], label: x[1] } : { value: x, label: x }
	);
	return { id, label, type: 'select', options: o, value: value ?? o[0].value };
};
export const toggle = (id: string, label: string, value = false, hint?: string): Control => ({
	id,
	label,
	type: 'toggle',
	value,
	hint
});
export const gpu = (id = 'gpu', label = 'GPU profile', value: GpuName = 'A100'): Control => ({
	id,
	label,
	type: 'gpu',
	value
});
