import { observeCanvasResize } from '../../widgets/widget-base.js';

/** @param {(context: CanvasRenderingContext2D, width: number, height: number) => void} draw */
export function createCanvasPlot(draw) {
	const canvas = document.createElement('canvas');
	canvas.className = 'viz-canvas';
	canvas.setAttribute('role', 'img');
	canvas.setAttribute('aria-label', 'Interactive mathematical visualization');
	const paint = () => {
		const rect = canvas.getBoundingClientRect();
		const context = canvas.getContext('2d');
		if (context && rect.width && rect.height) draw(context, rect.width, rect.height);
	};
	const disconnect = observeCanvasResize(canvas, paint);
	// `redraw` repaints on demand (after a control changed); resizing repaints by itself.
	return { element: canvas, destroy: disconnect, redraw: paint };
}
