// Tiny shared helpers reused by every Theory-tab widget in
// platform/widgets/ -- canvas sizing, slider binding, a readout
// formatter. Deliberately dependency-free (plain DOM/Canvas APIs) so
// each widget file itself stays small. See platform/widgets/README.md
// for the mount(root) -> cleanup contract every widget follows.

/**
 * Keeps a <canvas> sized to its CSS box (accounting for devicePixelRatio,
 * so lines stay crisp), and re-invokes `draw` after every resize.
 * The canvas starts out inside the hidden Theory panel (display:none
 * collapses it to 0x0 until the tab is opened), so a resize to 0x0 is
 * ignored rather than wiping the canvas and never drawing again.
 * Returns a disconnect function.
 * @param {HTMLCanvasElement} canvas
 * @param {() => void} draw
 */
export function observeCanvasResize(canvas, draw) {
	const ctx = /** @type {CanvasRenderingContext2D} */ (canvas.getContext('2d'));
	function resize() {
		const rect = canvas.getBoundingClientRect();
		if (rect.width === 0 || rect.height === 0) return;
		const dpr = window.devicePixelRatio || 1;
		canvas.width = rect.width * dpr;
		canvas.height = rect.height * dpr;
		ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
		draw();
	}
	const observer = new ResizeObserver(resize);
	observer.observe(canvas);
	resize();
	return () => observer.disconnect();
}

/**
 * Wires a <input type="range"> to a callback fired with its current
 * numeric value, both immediately and on every 'input' event. Returns
 * an unbind function.
 * @param {HTMLInputElement} el
 * @param {(value: number) => void} onInput
 */
export function bindRange(el, onInput) {
	const handler = () => onInput(parseFloat(el.value));
	el.addEventListener('input', handler);
	handler();
	return () => el.removeEventListener('input', handler);
}

/**
 * @param {number | string} x
 * @param {number} [digits]
 */
export function fmt(x, digits = 2) {
	return Number(x).toFixed(digits);
}
