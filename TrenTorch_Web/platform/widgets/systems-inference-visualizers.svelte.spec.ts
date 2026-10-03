import { afterEach, describe, expect, it, vi } from 'vitest';
import { curriculum } from 'virtual:curriculum/bundle';
import { mount } from './systems-inference-visualizers.js';
import { systemsVisualizerIds } from './systems-visualizer-ids.js';
import { widgetRegistry } from './registry.js';

const canvasContext = {
	clearRect: vi.fn(),
	fillRect: vi.fn(),
	beginPath: vi.fn(),
	moveTo: vi.fn(),
	lineTo: vi.fn(),
	stroke: vi.fn(),
	fillText: vi.fn(),
	arc: vi.fn(),
	fill: vi.fn(),
	strokeRect: vi.fn(),
	setTransform: vi.fn()
};

class TestResizeObserver {
	observe() {}
	disconnect() {}
}

describe('systems and inference visualizers', () => {
	afterEach(() => {
		vi.restoreAllMocks();
		vi.unstubAllGlobals();
		document.body.replaceChildren();
	});

	it('registers every visualizer slug used by the curriculum', () => {
		const curriculumIds = new Set(
			curriculum.roots.flatMap((root) =>
				root.sections.flatMap((section) =>
					section.tracks.flatMap((track) => track.questions.map((question) => question.id))
				)
			)
		);
		expect(systemsVisualizerIds).toHaveLength(40);
		expect(new Set(systemsVisualizerIds).size).toBe(systemsVisualizerIds.length);
		expect(systemsVisualizerIds.filter((id) => !curriculumIds.has(id))).toEqual([]);
		expect(systemsVisualizerIds.filter((id) => !(id in widgetRegistry))).toEqual([]);
	});

	it('mounts a resettable interactive widget for every brief slug', () => {
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

		for (const id of systemsVisualizerIds) {
			const root = document.createElement('div');
			root.dataset.widget = id;
			document.body.append(root);
			const cleanup = mount(root);

			expect(root.querySelector('h4')?.textContent, id).toBe('Try it live');
			expect(root.querySelector('canvas'), id).not.toBeNull();
			const sliderLabels = Array.from(
				root.querySelectorAll<HTMLInputElement>('input[type="range"]')
			).map((slider) => slider.getAttribute('aria-label'));
			expect(sliderLabels, id).not.toContain('Work items');
			expect(sliderLabels, id).not.toContain('Parameter value');
			expect(root.querySelector('.readout')?.textContent, id).not.toContain('active value');
			expect(
				Array.from(root.querySelectorAll('select option')).map((option) => option.textContent),
				id
			).not.toContain('Enabled');
			expect(
				Array.from(root.querySelectorAll<HTMLButtonElement>('button')).some(
					(button) => button.textContent === 'Reset'
				),
				id
			).toBe(true);
			if (!id.includes('timing') && !id.includes('vectorize')) {
				root.querySelector<HTMLButtonElement>('button.primary')?.click();
			}
			root.querySelector<HTMLButtonElement>('button:not(.primary)')?.click();
			cleanup();
			expect(root.childElementCount, id).toBe(0);
		}
	}, 15_000);
});
