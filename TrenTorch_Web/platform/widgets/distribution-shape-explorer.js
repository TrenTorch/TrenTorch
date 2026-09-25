// Widget for `math-pmf-and-pdf`: toggles between a discrete Binomial(n,p)
// bar chart (a PMF) and a continuous Uniform(a,b) density (a PDF), with
// live mean/variance readouts. Expects the markup shape from that
// question's README (a `[data-widget="distribution-shape-explorer"]` root
// containing #dcanvas, #discreteBtn/#continuousBtn, #nCtrl/#pCtrl/#aCtrl/
// #bCtrl with their sliders, and #roMean/#roVar readout spans).
import { observeCanvasResize, bindRange, fmt } from './widget-base.js';

/**
 * @param {number} n
 * @param {number} k
 * @returns {number}
 */
function choose(n, k) {
	if (k < 0 || k > n) return 0;
	let result = 1;
	for (let i = 0; i < k; i++) result = (result * (n - i)) / (i + 1);
	return result;
}

/**
 * @param {number} n
 * @param {number} p
 * @param {number} k
 */
function binomialPmf(n, p, k) {
	return choose(n, k) * p ** k * (1 - p) ** (n - k);
}

/** @param {HTMLElement} root */
export function mount(root) {
	const canvas = /** @type {HTMLCanvasElement} */ (root.querySelector('#dcanvas'));
	const discreteBtn = /** @type {HTMLButtonElement} */ (root.querySelector('#discreteBtn'));
	const continuousBtn = /** @type {HTMLButtonElement} */ (root.querySelector('#continuousBtn'));
	const nCtrl = /** @type {HTMLElement} */ (root.querySelector('#nCtrl'));
	const pCtrl = /** @type {HTMLElement} */ (root.querySelector('#pCtrl'));
	const aCtrl = /** @type {HTMLElement} */ (root.querySelector('#aCtrl'));
	const bCtrl = /** @type {HTMLElement} */ (root.querySelector('#bCtrl'));
	const nSlider = /** @type {HTMLInputElement} */ (root.querySelector('#nSlider'));
	const pSlider = /** @type {HTMLInputElement} */ (root.querySelector('#pSlider'));
	const aSlider = /** @type {HTMLInputElement} */ (root.querySelector('#aSlider'));
	const bSlider = /** @type {HTMLInputElement} */ (root.querySelector('#bSlider'));
	const nVal = /** @type {HTMLElement} */ (root.querySelector('#nVal'));
	const pVal = /** @type {HTMLElement} */ (root.querySelector('#pVal'));
	const aVal = /** @type {HTMLElement} */ (root.querySelector('#aVal'));
	const bVal = /** @type {HTMLElement} */ (root.querySelector('#bVal'));
	const roMean = /** @type {HTMLElement} */ (root.querySelector('#roMean'));
	const roVar = /** @type {HTMLElement} */ (root.querySelector('#roVar'));

	const ctx = /** @type {CanvasRenderingContext2D} */ (canvas.getContext('2d'));
	/** @type {'discrete' | 'continuous'} */
	let mode = 'discrete';

	function setMode(/** @type {'discrete' | 'continuous'} */ next) {
		mode = next;
		discreteBtn.classList.toggle('primary', mode === 'discrete');
		continuousBtn.classList.toggle('primary', mode === 'continuous');
		nCtrl.style.display = mode === 'discrete' ? '' : 'none';
		pCtrl.style.display = mode === 'discrete' ? '' : 'none';
		aCtrl.style.display = mode === 'continuous' ? '' : 'none';
		bCtrl.style.display = mode === 'continuous' ? '' : 'none';
		updateReadouts();
		draw();
	}

	function draw() {
		const w = canvas.clientWidth;
		const h = canvas.clientHeight;
		ctx.clearRect(0, 0, w, h);

		if (mode === 'discrete') {
			const n = parseInt(nSlider.value, 10);
			const p = parseFloat(pSlider.value);
			const pmfs = [];
			for (let k = 0; k <= n; k++) pmfs.push(binomialPmf(n, p, k));
			const maxPmf = Math.max(...pmfs, 1e-9);
			const barWidth = w / (n + 1);
			ctx.fillStyle = '#ef4444';
			for (let k = 0; k <= n; k++) {
				const barHeight = (pmfs[k] / maxPmf) * (h - 20);
				ctx.fillRect(k * barWidth + 2, h - barHeight, barWidth - 4, barHeight);
			}
		} else {
			const a = parseFloat(aSlider.value);
			const b = parseFloat(bSlider.value);
			const lo = Math.min(a, b);
			const hi = Math.max(a, b);
			const xMin = -6;
			const xMax = 6;
			const density = hi > lo ? 1 / (hi - lo) : 0;
			const yMax = Math.max(density * 1.3, 0.3);
			/** @param {number} x */
			const X = (x) => ((x - xMin) / (xMax - xMin)) * w;
			/** @param {number} y */
			const Y = (y) => h - (y / yMax) * (h - 20) - 10;

			ctx.fillStyle = 'rgba(239,68,68,0.28)';
			ctx.fillRect(X(lo), Y(density), X(hi) - X(lo), h - Y(density));
			ctx.strokeStyle = '#ef4444';
			ctx.lineWidth = 2;
			ctx.beginPath();
			ctx.moveTo(X(xMin), Y(0));
			ctx.lineTo(X(lo), Y(0));
			ctx.lineTo(X(lo), Y(density));
			ctx.lineTo(X(hi), Y(density));
			ctx.lineTo(X(hi), Y(0));
			ctx.lineTo(X(xMax), Y(0));
			ctx.stroke();
		}
	}

	function updateReadouts() {
		if (mode === 'discrete') {
			const n = parseInt(nSlider.value, 10);
			const p = parseFloat(pSlider.value);
			nVal.textContent = String(n);
			pVal.textContent = fmt(p, 2);
			roMean.textContent = fmt(n * p, 3);
			roVar.textContent = fmt(n * p * (1 - p), 3);
		} else {
			const a = parseFloat(aSlider.value);
			const b = parseFloat(bSlider.value);
			const lo = Math.min(a, b);
			const hi = Math.max(a, b);
			aVal.textContent = fmt(a, 1);
			bVal.textContent = fmt(b, 1);
			roMean.textContent = fmt((lo + hi) / 2, 3);
			roVar.textContent = fmt((hi - lo) ** 2 / 12, 3);
		}
	}

	function onDiscreteClick() {
		setMode('discrete');
	}
	function onContinuousClick() {
		setMode('continuous');
	}
	discreteBtn.addEventListener('click', onDiscreteClick);
	continuousBtn.addEventListener('click', onContinuousClick);

	const unbindN = bindRange(nSlider, () => {
		updateReadouts();
		draw();
	});
	const unbindP = bindRange(pSlider, () => {
		updateReadouts();
		draw();
	});
	const unbindA = bindRange(aSlider, () => {
		updateReadouts();
		draw();
	});
	const unbindB = bindRange(bSlider, () => {
		updateReadouts();
		draw();
	});

	const disconnectResize = observeCanvasResize(canvas, draw);
	setMode('discrete');

	return () => {
		discreteBtn.removeEventListener('click', onDiscreteClick);
		continuousBtn.removeEventListener('click', onContinuousClick);
		unbindN();
		unbindP();
		unbindA();
		unbindB();
		disconnectResize();
	};
}
