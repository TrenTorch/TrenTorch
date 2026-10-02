import { afterEach, describe, expect, it, vi } from 'vitest';
import { mount } from './math-visualizers.js';
import { mathVisualizerIds } from './math-visualizer-ids.js';

const canvasContext = {
	clearRect: vi.fn(),
	fillRect: vi.fn(),
	beginPath: vi.fn(),
	moveTo: vi.fn(),
	lineTo: vi.fn(),
	stroke: vi.fn(),
	setLineDash: vi.fn(),
	fillText: vi.fn(),
	arc: vi.fn(),
	fill: vi.fn(),
	setTransform: vi.fn()
};

class TestResizeObserver {
	observe() {}
	disconnect() {}
}

describe('math visualizer mounts', () => {
	afterEach(() => {
		vi.restoreAllMocks();
		vi.unstubAllGlobals();
		document.body.replaceChildren();
	});

	it('mounts a resettable Theory widget for every brief slug and cleans it up', () => {
		vi.stubGlobal('ResizeObserver', TestResizeObserver);
		vi.spyOn(HTMLCanvasElement.prototype, 'getContext').mockReturnValue(
			canvasContext as unknown as CanvasRenderingContext2D
		);
		vi.spyOn(HTMLCanvasElement.prototype, 'getBoundingClientRect').mockReturnValue({
			width: 600,
			height: 260,
			top: 0,
			right: 600,
			bottom: 260,
			left: 0,
			x: 0,
			y: 0,
			toJSON: () => ({})
		});

		for (const id of mathVisualizerIds) {
			const root = document.createElement('div');
			root.dataset.widget = id;
			document.body.append(root);
			const cleanup = mount(root);

			expect(root.querySelector('h4')?.textContent, id).toBe('Try it live');
			expect(
				Array.from(root.querySelectorAll('button.wbtn')).some(
					(button) => button.textContent === 'Reset'
				),
				id
			).toBe(true);

			cleanup();
			expect(root.childElementCount, id).toBe(0);
		}

		const seriesRoot = document.createElement('div');
		seriesRoot.dataset.widget = 'math-summation-notation';
		document.body.append(seriesRoot);
		const unmountSeries = mount(seriesRoot);
		seriesRoot.querySelector<HTMLButtonElement>('button.primary')?.click();
		expect(seriesRoot.querySelector('.readout')?.textContent).toContain('running sum1.000');
		Array.from(seriesRoot.querySelectorAll<HTMLButtonElement>('button'))
			.find((button) => button.textContent === 'Reset')
			?.click();
		expect(seriesRoot.querySelector('.readout')?.textContent).toContain('running sum0.000');
		unmountSeries();

		const samplerRoot = document.createElement('div');
		samplerRoot.dataset.widget = 'math-sampling-estimating-distribution';
		document.body.append(samplerRoot);
		const unmountSampler = mount(samplerRoot);
		samplerRoot.querySelector<HTMLButtonElement>('button.primary')?.click();
		expect(samplerRoot.querySelector('.readout')?.textContent).toContain('500');
		unmountSampler();
	});
});
