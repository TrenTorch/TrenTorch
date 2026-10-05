import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { curriculum } from 'virtual:curriculum/bundle';
import { mount } from './data-tools-visualizers.js';
import { dataToolsVisualizerIds } from './data-tools-visualizer-ids.js';
import { embeddedWidgetIds, widgetRegistry } from './registry.js';

const canvasContext = {
	clearRect: vi.fn(),
	fillRect: vi.fn(),
	strokeRect: vi.fn(),
	beginPath: vi.fn(),
	moveTo: vi.fn(),
	lineTo: vi.fn(),
	stroke: vi.fn(),
	fill: vi.fn(),
	arc: vi.fn(),
	fillText: vi.fn(),
	save: vi.fn(),
	restore: vi.fn(),
	translate: vi.fn(),
	rotate: vi.fn(),
	setTransform: vi.fn()
};

class TestResizeObserver {
	observe() {}
	disconnect() {}
}

function mountDemo(id: string) {
	const root = document.createElement('div');
	root.dataset.widget = id;
	document.body.append(root);
	const cleanup = mount(root);
	return { root, cleanup };
}

const readout = (root: HTMLElement, label: string) =>
	[...root.querySelectorAll('.readout div')]
		.find((row) => row.querySelector('span')?.textContent === label)
		?.querySelector('b')?.textContent;

function setRange(root: HTMLElement, label: string, value: number) {
	const input = root.querySelector<HTMLInputElement>(`input[aria-label="${label}"]`);
	if (!input) throw new Error(`no slider named ${label}`);
	input.value = String(value);
	input.dispatchEvent(new Event('input'));
}

function setSelect(root: HTMLElement, label: string, value: string) {
	const select = root.querySelector<HTMLSelectElement>(`select[aria-label="${label}"]`);
	if (!select) throw new Error(`no select named ${label}`);
	select.value = value;
	select.dispatchEvent(new Event('change'));
}

function toggle(root: HTMLElement, text: string) {
	const label = [...root.querySelectorAll('label.wtoggle')].find((l) =>
		l.textContent?.includes(text)
	);
	const input = label?.querySelector('input');
	if (!input) throw new Error(`no toggle containing ${text}`);
	input.checked = !input.checked;
	input.dispatchEvent(new Event('change'));
}

const rowCount = (root: HTMLElement, tableIndex: number) =>
	root.querySelectorAll('.wtable')[tableIndex].querySelectorAll('tbody tr').length;

describe('data tools visualizers', () => {
	beforeEach(() => {
		vi.stubGlobal('ResizeObserver', TestResizeObserver);
		vi.spyOn(HTMLCanvasElement.prototype, 'getContext').mockReturnValue(
			canvasContext as unknown as CanvasRenderingContext2D
		);
		vi.spyOn(HTMLCanvasElement.prototype, 'getBoundingClientRect').mockReturnValue({
			width: 600,
			height: 320,
			top: 0,
			right: 600,
			bottom: 320,
			left: 0,
			x: 0,
			y: 0,
			toJSON: () => ({})
		});
	});

	afterEach(() => {
		vi.restoreAllMocks();
		vi.unstubAllGlobals();
		document.body.replaceChildren();
	});

	it('registers every demo, and each one is placed in a question that exists', () => {
		const questions = curriculum.roots.flatMap((root) =>
			root.sections.flatMap((section) => section.tracks.flatMap((track) => track.questions))
		);
		expect(new Set(dataToolsVisualizerIds).size).toBe(dataToolsVisualizerIds.length);
		expect(dataToolsVisualizerIds.filter((id) => !(id in widgetRegistry))).toEqual([]);
		for (const id of dataToolsVisualizerIds) {
			const used = questions.filter((q) => embeddedWidgetIds(q.theoryMarkdown).includes(id));
			expect(used.length, `${id} is not placed in any question's Theory`).toBeGreaterThan(0);
		}
	});

	it('mounts a titled widget for every id and cleans up after itself', () => {
		for (const id of dataToolsVisualizerIds) {
			const { root, cleanup } = mountDemo(id);
			expect(root.querySelector('h4')?.textContent, id).toBe('Try it live');
			expect(root.classList.contains('tt-widget'), id).toBe(true);
			cleanup();
			expect(root.childElementCount, id).toBe(0);
		}
	});

	it('ignores a root that is not one of its demos', () => {
		const { root, cleanup } = mountDemo('math-dot-product-norms');
		expect(root.childElementCount).toBe(0);
		cleanup();
	});

	it('loc includes its end label and iloc excludes its end position', () => {
		const { root } = mountDemo('data-science-pandas-label-vs-position');
		expect(readout(root, 'loc rows')).toBe('3'); // labels 20, 30, 40
		expect(readout(root, 'iloc rows')).toBe('2'); // positions 1, 2
		setRange(root, 'loc to label', 20);
		expect(readout(root, 'loc rows')).toBe('1'); // 20:20 still returns a row
		setRange(root, 'iloc to position', 1);
		expect(readout(root, 'iloc rows')).toBe('0'); // 1:1 is empty
	});

	it('aggregate gives one row per group, transform keeps every row, head keeps one per group', () => {
		const { root } = mountDemo('data-science-pandas-groupby-aggregate');
		expect(rowCount(root, 0)).toBe(6);
		expect(readout(root, 'rows out')).toBe('3');
		setSelect(root, 'apply', 'transform');
		expect(readout(root, 'rows out')).toBe('6');
		setSelect(root, 'apply', 'head (top 1)');
		expect(readout(root, 'rows out')).toBe('3');
		expect(root.querySelector('.wcode:nth-of-type(1)')).not.toBeNull();
	});

	it('shows each join type with its own number of rows, and a duplicate key multiplies them', () => {
		const { root } = mountDemo('data-science-pandas-merge-join');
		const rows = () => readout(root, 'rows out');
		setSelect(root, 'how', 'inner');
		expect(rows()).toBe('2');
		setSelect(root, 'how', 'left');
		expect(rows()).toBe('3');
		setSelect(root, 'how', 'right');
		expect(rows()).toBe('3');
		setSelect(root, 'how', 'outer');
		expect(rows()).toBe('4');
		toggle(root, 'duplicate key');
		expect(rows()).toBe('5'); // customer 1 now matches two orders
		setSelect(root, 'how', 'inner');
		expect(rows()).toBe('3');
	});

	it('the aggregation function decides what the doubled cell shows', () => {
		const { root } = mountDemo('data-science-pandas-pivot-crosstab');
		expect(readout(root, 'north · Q1 shows')).toBe('12');
		setSelect(root, 'aggfunc', 'mean');
		expect(readout(root, 'north · Q1 shows')).toBe('6');
		setSelect(root, 'aggfunc', 'count');
		expect(readout(root, 'north · Q1 shows')).toBe('2');
		expect(readout(root, 'empty cells')).toBe('4');
		toggle(root, 'fill_value=0');
		expect(readout(root, 'empty cells')).toBe('0');
		toggle(root, 'melt');
		expect(root.querySelectorAll('.wtable')[1].querySelectorAll('tbody tr').length).toBe(9);
	});

	it('names the object behind each part of a chart', () => {
		const { root } = mountDemo('data-science-matplotlib-figure-axes-lines');
		const items = [...root.querySelectorAll<HTMLButtonElement>('.wtree-item')];
		expect(items.map((item) => item.textContent)).toContain('ax.lines[0]');
		items.find((item) => item.textContent === 'ax.title')?.click();
		expect(readout(root, 'object')).toBe('ax.title');
	});

	it('pinning the colour scale changes what the colours mean', () => {
		const { root } = mountDemo('data-science-seaborn-heatmaps-correlation');
		expect(readout(root, 'scale')).toContain('automatic');
		toggle(root, 'pin the colour scale');
		expect(readout(root, 'scale')).toBe('pinned -1.0 … 1.0');
		setRange(root, 'zmax', 0.5);
		expect(readout(root, 'scale')).toBe('pinned -1.0 … 0.5');
	});

	it('bins and bandwidth readouts follow the sliders, and Scott’s rule button resets the bandwidth', () => {
		const { root } = mountDemo('data-science-seaborn-distribution-plots');
		const before = readout(root, 'bin width');
		setRange(root, 'bins', 20);
		expect(readout(root, 'bin width')).not.toBe(before);
		setRange(root, 'KDE bandwidth', 1.5);
		expect(readout(root, 'bandwidth')).toBe('1.50');
		root.querySelector<HTMLButtonElement>('button.wbtn')?.click();
		expect(readout(root, 'bandwidth')).toBe(readout(root, "Scott's rule"));
	});

	it('fixed ranges keep the axes the same in every frame, autoscaling does not', () => {
		const { root } = mountDemo('data-science-plotly-animation-frames');
		expect(readout(root, 'axes')).toBe('fixed for all frames');
		setRange(root, 'frame', 2);
		expect(readout(root, 'frame')).toBe('2020');
		const fixedRange = readout(root, 'x range');
		toggle(root, 'fix the axis ranges');
		expect(readout(root, 'axes')).toBe('rescaled every frame');
		expect(readout(root, 'x range')).not.toBe(fixedRange);
	});
});
