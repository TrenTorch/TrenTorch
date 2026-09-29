import { afterEach, describe, expect, it, vi } from 'vitest';
import { linearNoisy, twoBlobs } from './classical-ml-datasets.js';
import { classicalMLVisualizerIds } from './classical-ml-visualizer-ids.js';
import { mount } from './classical-ml-visualizers.js';
import { widgetRegistry } from './registry.js';

const canvasContext = {
	canvas: {
		width: 600,
		height: 300,
		clientWidth: 600,
		clientHeight: 300
	},
	clearRect: vi.fn(),
	fillRect: vi.fn(),
	beginPath: vi.fn(),
	save: vi.fn(),
	restore: vi.fn(),
	rect: vi.fn(),
	clip: vi.fn(),
	moveTo: vi.fn(),
	lineTo: vi.fn(),
	stroke: vi.fn(),
	setLineDash: vi.fn(),
	fillText: vi.fn(),
	arc: vi.fn(),
	ellipse: vi.fn(),
	fill: vi.fn(),
	strokeRect: vi.fn(),
	closePath: vi.fn(),
	setTransform: vi.fn()
};

class TestResizeObserver {
	observe() {}
	disconnect() {}
}

describe('Classical ML and Data visualizers', () => {
	afterEach(() => {
		vi.restoreAllMocks();
		vi.unstubAllGlobals();
		document.body.replaceChildren();
	});

	it('registers the complete 47-question brief catalog', () => {
		expect(classicalMLVisualizerIds).toHaveLength(47);
		expect(new Set(classicalMLVisualizerIds).size).toBe(47);
		expect(classicalMLVisualizerIds.filter((id) => !(id in widgetRegistry))).toEqual([]);
	});

	it('generates repeatable shared datasets from the seeded generators', () => {
		expect(linearNoisy(8)).toEqual(linearNoisy(8));
		expect(twoBlobs()).toEqual(twoBlobs());
		expect(new Set(twoBlobs().map((point) => point.label))).toEqual(new Set([0, 1]));
	});

	it('mounts an interactive resettable widget for every brief slug', () => {
		vi.stubGlobal('ResizeObserver', TestResizeObserver);
		vi.spyOn(HTMLCanvasElement.prototype, 'getContext').mockReturnValue(
			canvasContext as unknown as CanvasRenderingContext2D
		);
		vi.spyOn(HTMLCanvasElement.prototype, 'getBoundingClientRect').mockReturnValue({
			width: 600,
			height: 300,
			top: 0,
			right: 600,
			bottom: 300,
			left: 0,
			x: 0,
			y: 0,
			toJSON: () => ({})
		});

		for (const id of classicalMLVisualizerIds) {
			const root = document.createElement('div');
			root.dataset.widget = id;
			document.body.append(root);
			const cleanup = mount(root);
			expect(root.querySelector('h4')?.textContent, id).toBe('Try it live');
			expect(root.querySelector('canvas'), id).not.toBeNull();
			expect(canvasContext.clearRect).toHaveBeenCalledWith(0, 0, 600, 300);
			expect(root.querySelector('.viz-caption')?.textContent, id).toBeTruthy();
			expect(
				Array.from(root.querySelectorAll('button')).some(
					(button) => button.textContent === 'Reset'
				),
				id
			).toBe(true);
			root.querySelector<HTMLButtonElement>('button.primary')?.click();
			root.querySelector<HTMLButtonElement>('button:not(.primary)')?.click();
			cleanup();
			expect(root.childElementCount, id).toBe(0);
		}
	}, 15_000);

	it('makes data, statistics, and model action buttons update their output', () => {
		vi.stubGlobal('ResizeObserver', TestResizeObserver);
		vi.spyOn(HTMLCanvasElement.prototype, 'getContext').mockReturnValue(
			canvasContext as unknown as CanvasRenderingContext2D
		);
		vi.spyOn(HTMLCanvasElement.prototype, 'getBoundingClientRect').mockReturnValue({
			width: 600,
			height: 300,
			top: 0,
			right: 600,
			bottom: 300,
			left: 0,
			x: 0,
			y: 0,
			toJSON: () => ({})
		});

		for (const id of [
			'math-detecting-missing-values',
			'math-confidence-interval',
			'linear-regression-training-loop',
			'classification-training-loop',
			'regularized-linear-models-ridge-regression',
			'support-vector-machines-margin-maximization'
		]) {
			const root = document.createElement('div');
			root.dataset.widget = id;
			document.body.append(root);
			const cleanup = mount(root);
			const output = root.querySelector('.readout');
			const initialOutput = output?.textContent;
			const initialDraws = canvasContext.clearRect.mock.calls.length;

			root.querySelector<HTMLButtonElement>('button.primary')?.click();

			expect(canvasContext.clearRect.mock.calls.length, id).toBeGreaterThan(initialDraws);
			if (id === 'classification-training-loop') {
				expect(root.querySelector<HTMLInputElement>('input[type="range"]')?.value, id).not.toBe(
					'0.8'
				);
			} else {
				expect(output?.textContent, id).not.toBe(initialOutput);
			}
			cleanup();
		}
	});
});
