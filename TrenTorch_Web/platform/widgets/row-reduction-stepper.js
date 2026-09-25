// Widget for `math-gaussian-elimination`: steps through row-reducing a
// fixed augmented matrix [A|b] one pivot at a time, highlighting the
// current pivot cell and the cells changed by that step. Expects a
// `[data-widget="row-reduction-stepper"]` root containing `.matrix-grid`,
// `#stepBackBtn`, `#stepForwardBtn`, `#resetBtn`, `#stepLabel`, and
// `#stepDescription`.

// The example system: 2x + y - z = 8, -3x - y + 2z = -11, -2x + y + 2z = -3
// (solution x=2, y=3, z=-1) -- the same worked example used throughout
// this module's Theory.
const EXAMPLE_MATRIX = [
	[2, 1, -1, 8],
	[-3, -1, 2, -11],
	[-2, 1, 2, -3]
];

/**
 * Runs Gaussian elimination on `matrix`, recording a snapshot after
 * every pivot's elimination step.
 * @param {number[][]} matrix
 * @returns {{grid: number[][], pivot: [number, number] | null, changed: [number, number][], description: string}[]}
 */
function computeSteps(matrix) {
	const rows = matrix.length;
	const cols = matrix[0].length;
	/** @type {number[][]} */
	let M = matrix.map((row) => [...row]);

	/** @type {{grid: number[][], pivot: [number, number] | null, changed: [number, number][], description: string}[]} */
	const steps = [
		{
			grid: M.map((row) => [...row]),
			pivot: null,
			changed: [],
			description: 'Starting augmented matrix [A | b].'
		}
	];

	for (let pivotRow = 0; pivotRow < rows - 1; pivotRow++) {
		const pivotCol = pivotRow;
		/** @type {[number, number][]} */
		const changed = [];
		const newM = M.map((row) => [...row]);
		for (let r = pivotRow + 1; r < rows; r++) {
			const multiplier = M[r][pivotCol] / M[pivotRow][pivotCol];
			for (let c = 0; c < cols; c++) {
				newM[r][c] = M[r][c] - multiplier * M[pivotRow][c];
				changed.push([r, c]);
			}
		}
		M = newM;
		steps.push({
			grid: M.map((row) => [...row]),
			pivot: [pivotRow, pivotCol],
			changed,
			description: `Eliminate column ${pivotCol + 1} below row ${pivotRow + 1}, using it as the pivot.`
		});
	}

	steps.push({
		grid: M.map((row) => [...row]),
		pivot: null,
		changed: [],
		description: 'Done -- upper-triangular. Back-substitution solves the rest.'
	});

	return steps;
}

/** @param {number} x */
function fmtCell(x) {
	const rounded = Math.round(x * 100) / 100;
	return Object.is(rounded, -0) ? '0' : String(rounded);
}

/** @param {HTMLElement} root */
export function mount(root) {
	const grid = /** @type {HTMLElement} */ (root.querySelector('.matrix-grid'));
	const stepBackBtn = /** @type {HTMLButtonElement} */ (root.querySelector('#stepBackBtn'));
	const stepForwardBtn = /** @type {HTMLButtonElement} */ (root.querySelector('#stepForwardBtn'));
	const resetBtn = /** @type {HTMLButtonElement} */ (root.querySelector('#resetBtn'));
	const stepLabel = /** @type {HTMLElement} */ (root.querySelector('#stepLabel'));
	const stepDescription = /** @type {HTMLElement} */ (root.querySelector('#stepDescription'));

	const steps = computeSteps(EXAMPLE_MATRIX);
	let current = 0;

	function render() {
		const step = steps[current];
		grid.innerHTML = '';
		step.grid.forEach((row, r) => {
			const rowEl = document.createElement('div');
			rowEl.className = 'matrix-row';
			row.forEach((value, c) => {
				const cell = document.createElement('div');
				const isAugmented = c === row.length - 1;
				const isPivot = step.pivot && step.pivot[0] === r && step.pivot[1] === c;
				const isChanged = step.changed.some(([cr, cc]) => cr === r && cc === c);
				cell.className =
					'matrix-cell' +
					(isAugmented ? ' augmented' : '') +
					(isPivot ? ' pivot' : '') +
					(isChanged && !isPivot ? ' changed' : '');
				cell.textContent = fmtCell(value);
				rowEl.appendChild(cell);
			});
			grid.appendChild(rowEl);
		});

		stepLabel.textContent = `${current} / ${steps.length - 1}`;
		stepDescription.textContent = step.description;
		stepBackBtn.disabled = current === 0;
		stepForwardBtn.disabled = current === steps.length - 1;
	}

	function onBack() {
		if (current > 0) {
			current -= 1;
			render();
		}
	}
	function onForward() {
		if (current < steps.length - 1) {
			current += 1;
			render();
		}
	}
	function onReset() {
		current = 0;
		render();
	}

	stepBackBtn.addEventListener('click', onBack);
	stepForwardBtn.addEventListener('click', onForward);
	resetBtn.addEventListener('click', onReset);

	render();

	return () => {
		stepBackBtn.removeEventListener('click', onBack);
		stepForwardBtn.removeEventListener('click', onForward);
		resetBtn.removeEventListener('click', onReset);
	};
}
