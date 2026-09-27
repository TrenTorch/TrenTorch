// Widget for `math-probability-gaussian-distribution`: a live μ/σ slider
// reshaping the Gaussian PDF curve, plus a "draw samples" button that
// overlays a histogram from a JS re-implementation of the question's own
// Box-Muller sampling. Expects the markup shape from that question's
// README (a `[data-widget="gaussian-distribution"]` root containing
// #gcanvas, #muSlider, #sigmaSlider, #drawBtn, #resetBtn, and the
// #roMu/#roSigma/#roN/#roMean/#roStd readout spans).
import { observeCanvasResize, bindRange, fmt } from './widget-base.js';

/**
 * @param {number} x
 * @param {number} mu
 * @param {number} sigma
 */
function pdf(x, mu, sigma) {
	const coeff = 1 / (sigma * Math.sqrt(2 * Math.PI));
	return coeff * Math.exp(-((x - mu) ** 2) / (2 * sigma * sigma));
}

// Mirrors the question's own Box-Muller sample_gaussian, using
// Math.random() in place of pre-generated uniform draws.
/**
 * @param {number} mu
 * @param {number} sigma
 * @param {number} n
 * @returns {number[]}
 */
function drawSamples(mu, sigma, n) {
	const out = [];
	while (out.length < n) {
		const u1 = Math.max(Math.random(), 1e-12);
		const u2 = Math.random();
		const r = Math.sqrt(-2 * Math.log(u1));
		const theta = 2 * Math.PI * u2;
		out.push(mu + sigma * r * Math.cos(theta));
		out.push(mu + sigma * r * Math.sin(theta));
	}
	return out.slice(0, n);
}

/** @param {HTMLElement} root */
export function mount(root) {
	const canvas = /** @type {HTMLCanvasElement} */ (root.querySelector('#gcanvas'));
	const muSlider = /** @type {HTMLInputElement} */ (root.querySelector('#muSlider'));
	const sigmaSlider = /** @type {HTMLInputElement} */ (root.querySelector('#sigmaSlider'));
	const muVal = /** @type {HTMLElement} */ (root.querySelector('#muVal'));
	const sigmaVal = /** @type {HTMLElement} */ (root.querySelector('#sigmaVal'));
	const roMu = /** @type {HTMLElement} */ (root.querySelector('#roMu'));
	const roSigma = /** @type {HTMLElement} */ (root.querySelector('#roSigma'));
	const roN = /** @type {HTMLElement} */ (root.querySelector('#roN'));
	const roMean = /** @type {HTMLElement} */ (root.querySelector('#roMean'));
	const roStd = /** @type {HTMLElement} */ (root.querySelector('#roStd'));
	const drawBtn = /** @type {HTMLButtonElement} */ (root.querySelector('#drawBtn'));
	const resetBtn = /** @type {HTMLButtonElement} */ (root.querySelector('#resetBtn'));

	/** @type {number[]} */
	let samples = [];
	const ctx = /** @type {CanvasRenderingContext2D} */ (canvas.getContext('2d'));

	function draw() {
		const w = canvas.clientWidth;
		const h = canvas.clientHeight;
		ctx.clearRect(0, 0, w, h);

		const mu = parseFloat(muSlider.value);
		const sigma = parseFloat(sigmaSlider.value);
		const xMin = -8;
		const xMax = 8;
		const yMax = pdf(mu, mu, sigma) * 1.15;

		/** @param {number} x */
		const X = (x) => ((x - xMin) / (xMax - xMin)) * w;
		/** @param {number} y */
		const Y = (y) => h - (y / yMax) * (h - 20) - 10;

		ctx.strokeStyle = 'rgba(255,255,255,0.06)';
		ctx.lineWidth = 1;
		for (let gx = xMin; gx <= xMax; gx += 2) {
			ctx.beginPath();
			ctx.moveTo(X(gx), 0);
			ctx.lineTo(X(gx), h);
			ctx.stroke();
		}

		if (samples.length) {
			const bins = 40;
			const counts = new Array(bins).fill(0);
			samples.forEach((s) => {
				const bi = Math.floor(((s - xMin) / (xMax - xMin)) * bins);
				if (bi >= 0 && bi < bins) counts[bi]++;
			});
			const binWidth = (xMax - xMin) / bins;
			const maxDensity = Math.max(...counts.map((c) => c / (samples.length * binWidth)));
			const scale = maxDensity > yMax ? (yMax / maxDensity) * 0.95 : 1;
			ctx.fillStyle = 'rgba(239,68,68,0.28)';
			counts.forEach((c, i) => {
				const density = (c / (samples.length * binWidth)) * scale;
				const x0 = X(xMin + i * binWidth);
				const x1 = X(xMin + (i + 1) * binWidth);
				ctx.fillRect(x0, Y(density), Math.max(x1 - x0 - 1, 1), h - Y(density));
			});
		}

		ctx.strokeStyle = '#ef4444';
		ctx.lineWidth = 2;
		ctx.beginPath();
		for (let px = 0; px <= w; px++) {
			const x = xMin + (px / w) * (xMax - xMin);
			const y = pdf(x, mu, sigma);
			const py = Y(y);
			if (px === 0) ctx.moveTo(px, py);
			else ctx.lineTo(px, py);
		}
		ctx.stroke();

		ctx.strokeStyle = 'rgba(240,180,41,0.7)';
		ctx.setLineDash([4, 4]);
		ctx.beginPath();
		ctx.moveTo(X(mu), 0);
		ctx.lineTo(X(mu), h);
		ctx.stroke();
		ctx.setLineDash([]);
	}

	function updateReadouts() {
		muVal.textContent = fmt(muSlider.value, 1);
		sigmaVal.textContent = fmt(sigmaSlider.value, 1);
		roMu.textContent = fmt(muSlider.value, 2);
		roSigma.textContent = fmt(sigmaSlider.value, 2);
		roN.textContent = String(samples.length);
		if (samples.length) {
			const mean = samples.reduce((a, b) => a + b, 0) / samples.length;
			const std = Math.sqrt(samples.reduce((a, b) => a + (b - mean) ** 2, 0) / samples.length);
			roMean.textContent = fmt(mean, 3);
			roStd.textContent = fmt(std, 3);
		} else {
			roMean.textContent = '—';
			roStd.textContent = '—';
		}
	}

	const unbindMu = bindRange(muSlider, () => {
		updateReadouts();
		draw();
	});
	const unbindSigma = bindRange(sigmaSlider, () => {
		updateReadouts();
		draw();
	});

	function onDraw() {
		const mu = parseFloat(muSlider.value);
		const sigma = parseFloat(sigmaSlider.value);
		samples = drawSamples(mu, sigma, 500);
		updateReadouts();
		draw();
	}
	function onReset() {
		samples = [];
		updateReadouts();
		draw();
	}
	drawBtn.addEventListener('click', onDraw);
	resetBtn.addEventListener('click', onReset);

	const disconnectResize = observeCanvasResize(canvas, draw);
	updateReadouts();

	return () => {
		unbindMu();
		unbindSigma();
		drawBtn.removeEventListener('click', onDraw);
		resetBtn.removeEventListener('click', onReset);
		disconnectResize();
	};
}
