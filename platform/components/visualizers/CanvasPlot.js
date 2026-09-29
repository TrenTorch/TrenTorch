import { observeCanvasResize } from '../../widgets/widget-base.js';

/** @param {(context: CanvasRenderingContext2D, width: number, height: number) => void} draw */
export function createCanvasPlot(draw) {
	const canvas = document.createElement('canvas');
	canvas.className = 'viz-canvas';
	canvas.setAttribute('role', 'img');
	canvas.setAttribute('aria-label', 'Interactive mathematical visualization');
	const disconnect = observeCanvasResize(canvas, () => {
		const rect = canvas.getBoundingClientRect();
		const context = canvas.getContext('2d');
		if (context && rect.width && rect.height) draw(context, rect.width, rect.height);
	});
	return { element: canvas, destroy: disconnect };
}
