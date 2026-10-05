// Live demos for the pandas and chart-library questions. One module, one mount(root) that picks
// the demo from root.dataset.widget (same contract as math-visualizers.js and the other families).
// Plain DOM and canvas, seeded data, no dependencies. Every demo is deterministic so a screenshot
// or a test always sees the same picture.
import { createSlider } from '../components/visualizers/Slider.js';
import { createStatsPanel } from '../components/visualizers/StatsPanel.js';
import { createActionButton } from '../components/visualizers/ActionButton.js';
import { createCanvasPlot } from '../components/visualizers/CanvasPlot.js';
import { seededRandom } from '../components/visualizers/seededRandom.js';
import { dataToolsVisualizerIds } from './data-tools-visualizer-ids.js';

const GROUP_COLOURS = ['#60a5fa', '#f59e0b', '#34d399', '#f472b6', '#a78bfa'];

/**
 * @param {string} tag
 * @param {Record<string, string>} [attributes]
 * @param {(Node | string)[]} [children]
 */
function el(tag, attributes = {}, children = []) {
	const node = document.createElement(tag);
	for (const [name, value] of Object.entries(attributes)) node.setAttribute(name, value);
	node.append(...children);
	return node;
}

/** @param {string} label @param {string[]} options @param {string} value @param {(value: string) => void} onChange */
function createSelect(label, options, value, onChange) {
	const select = /** @type {HTMLSelectElement} */ (el('select', { 'aria-label': label }));
	for (const option of options) select.append(el('option', { value: option }, [option]));
	select.value = value;
	select.addEventListener('change', () => onChange(select.value));
	const wrapper = el('div', { class: 'ctrl' }, [
		el('label', {}, [el('span', {}, [label])]),
		select
	]);
	return { element: wrapper, select };
}

/** @param {string} label @param {boolean} checked @param {(value: boolean) => void} onChange */
function createToggle(label, checked, onChange) {
	const input = /** @type {HTMLInputElement} */ (el('input', { type: 'checkbox' }));
	input.checked = checked;
	input.addEventListener('change', () => onChange(input.checked));
	return { element: el('label', { class: 'wtoggle' }, [input, ` ${label}`]), input };
}

/**
 * A table of rows. `rowClass(row, i)` may return 'sel' (highlight) or a group colour index as 'g0'..'g4'.
 * @param {string[]} columns
 * @param {(string | number | null)[][]} rows
 * @param {(row: (string | number | null)[], index: number) => string} [rowClass]
 */
function table(columns, rows, rowClass = () => '') {
	const head = el(
		'tr',
		{},
		columns.map((name) => el('th', {}, [name]))
	);
	const body = rows.map((row, index) => {
		const tr = el('tr', { class: rowClass(row, index) });
		for (const cell of row) {
			tr.append(cell === null ? el('td', { class: 'nan' }, ['NaN']) : el('td', {}, [String(cell)]));
		}
		return tr;
	});
	return el('table', { class: 'wtable' }, [el('thead', {}, [head]), el('tbody', {}, body)]);
}

/** @param {string} id @param {string} title @param {string} caption */
function scaffold(id, title, caption) {
	const shell = el('section', { class: 'tt-math-viz tt-data-viz', 'data-demo': id });
	const stage = el('div', { class: 'viz-stage' });
	const controls = el('div', { class: 'viz-controls controls' });
	const stats = createStatsPanel();
	shell.append(
		el('h4', {}, [title]),
		stage,
		controls,
		el('p', { class: 'viz-caption' }, [caption])
	);
	return { shell, stage, controls, stats };
}

/** @typedef {{ shell: HTMLElement; destroy?: () => void }} Demo */

// ---------------------------------------------------------------- label vs position
/** @returns {Demo} */
function labelVsPosition() {
	const labels = [10, 20, 30, 40, 50];
	const rows = [
		['Pune', 31],
		['Delhi', 38],
		['Goa', 29],
		['Agra', 40],
		['Kochi', 30]
	];
	const state = { labelFrom: 20, labelTo: 40, posFrom: 1, posTo: 3 };
	const { shell, stage, controls, stats } = scaffold(
		'label-vs-position',
		'Try it live',
		'Both calls ask for "rows 20 to 40" and "rows 1 to 3". They return different rows because the index is not 0, 1, 2, …'
	);
	const labelFrom = createSlider({
		label: 'loc from label',
		min: 10,
		max: 50,
		step: 10,
		value: 20
	});
	const labelTo = createSlider({ label: 'loc to label', min: 10, max: 50, step: 10, value: 40 });
	const posFrom = createSlider({ label: 'iloc from position', min: 0, max: 5, step: 1, value: 1 });
	const posTo = createSlider({ label: 'iloc to position', min: 0, max: 5, step: 1, value: 3 });
	controls.append(
		labelFrom.element,
		labelTo.element,
		posFrom.element,
		posTo.element,
		stats.element
	);
	const view = el('div', { class: 'wgrid' });
	stage.append(view);

	function render() {
		const byLabel = labels.map((l) => l >= state.labelFrom && l <= state.labelTo);
		const byPosition = labels.map((_, i) => i >= state.posFrom && i < state.posTo);
		const build = (/** @type {boolean[]} */ picked) =>
			table(
				['pos', 'label', 'city', 'temp'],
				labels.map((label, i) => [i, label, rows[i][0], rows[i][1]]),
				(_row, i) => (picked[i] ? 'sel' : '')
			);
		view.replaceChildren(
			el('div', {}, [
				el('div', { class: 'wcode' }, [
					`df.loc[${state.labelFrom}:${state.labelTo}]  # label slice: end included`
				]),
				build(byLabel)
			]),
			el('div', {}, [
				el('div', { class: 'wcode' }, [
					`df.iloc[${state.posFrom}:${state.posTo}]  # position slice: end excluded`
				]),
				build(byPosition)
			])
		);
		stats.update([
			{ label: 'loc rows', value: byLabel.filter(Boolean).length },
			{ label: 'iloc rows', value: byPosition.filter(Boolean).length }
		]);
	}
	for (const [slider, key] of /** @type {const} */ ([
		[labelFrom, 'labelFrom'],
		[labelTo, 'labelTo'],
		[posFrom, 'posFrom'],
		[posTo, 'posTo']
	])) {
		slider.input.addEventListener('input', () => {
			state[key] = Number(slider.input.value);
			render();
		});
	}
	render();
	return { shell };
}

// ---------------------------------------------------------------- groupby
/** @returns {Demo} */
function groupBySplitApply() {
	const data = [
		['ops', 'A', 50],
		['dev', 'B', 70],
		['dev', 'C', 90],
		['ops', 'D', 60],
		['dev', 'E', 80],
		['hr', 'F', 40]
	];
	const depts = /** @type {string[]} */ ([...new Set(data.map((row) => String(row[0])))]);
	const state = { apply: 'aggregate', func: 'mean' };
	const { shell, stage, controls, stats } = scaffold(
		'groupby',
		'Try it live',
		'Same split, three different ways to combine. Aggregate collapses each group to one row, transform keeps every row, head keeps some rows.'
	);
	const apply = createSelect(
		'apply',
		['aggregate', 'transform', 'head (top 1)'],
		'aggregate',
		(value) => {
			state.apply = value;
			render();
		}
	);
	const func = createSelect('function', ['mean', 'sum', 'count', 'max'], 'mean', (value) => {
		state.func = value;
		render();
	});
	controls.append(apply.element, func.element, stats.element);
	const view = el('div', { class: 'wgrid' });
	stage.append(view);

	/** @param {number[]} values */
	const reduce = (values) => {
		if (state.func === 'sum') return values.reduce((a, b) => a + b, 0);
		if (state.func === 'count') return values.length;
		if (state.func === 'max') return Math.max(...values);
		return Math.round((values.reduce((a, b) => a + b, 0) / values.length) * 100) / 100;
	};

	function render() {
		const groupClass = (/** @type {(string|number|null)[]} */ row) =>
			`g${depts.indexOf(String(row[0]))}`;
		const salaries = (/** @type {string} */ dept) =>
			data.filter((row) => row[0] === dept).map((row) => /** @type {number} */ (row[2]));
		let code;
		/** @type {(string|number|null)[][]} */
		let out;
		let columns;
		if (state.apply === 'aggregate') {
			code = `df.groupby("dept")["salary"].agg("${state.func}")`;
			columns = ['dept', `salary_${state.func}`];
			out = depts.map((dept) => [dept, reduce(salaries(dept))]);
		} else if (state.apply === 'transform') {
			code = `df["salary_group_${state.func}"] = df.groupby("dept")["salary"].transform("${state.func}")`;
			columns = ['dept', 'name', 'salary', `group_${state.func}`];
			out = data.map((row) => [row[0], row[1], row[2], reduce(salaries(String(row[0])))]);
		} else {
			code = 'df.sort_values("salary", ascending=False).groupby("dept").head(1)';
			columns = ['dept', 'name', 'salary'];
			out = depts.map((dept) => {
				const best = data
					.filter((row) => row[0] === dept)
					.sort((a, b) => /** @type {number} */ (b[2]) - /** @type {number} */ (a[2]))[0];
				return [best[0], best[1], best[2]];
			});
		}
		view.replaceChildren(
			el('div', {}, [
				el('div', { class: 'wcode' }, ['df  # 6 rows, 3 groups']),
				table(['dept', 'name', 'salary'], data, groupClass)
			]),
			el('div', {}, [el('div', { class: 'wcode' }, [code]), table(columns, out, groupClass)])
		);
		stats.update([
			{ label: 'rows in', value: data.length },
			{ label: 'rows out', value: out.length }
		]);
	}
	render();
	return { shell };
}

// ---------------------------------------------------------------- merge
/** @returns {Demo} */
function joinTypes() {
	const customers = [
		[1, 'Asha'],
		[2, 'Ben'],
		[3, 'Cara']
	];
	const state = { how: 'left', duplicate: false };
	const { shell, stage, controls, stats } = scaffold(
		'merge',
		'Try it live',
		'Unmatched rows are kept or dropped depending on the join type, and a key that appears twice on one side multiplies the rows.'
	);
	const how = createSelect('how', ['inner', 'left', 'right', 'outer'], 'left', (value) => {
		state.how = value;
		render();
	});
	const duplicate = createToggle('second order for customer 1 (duplicate key)', false, (value) => {
		state.duplicate = value;
		render();
	});
	controls.append(how.element, duplicate.element, stats.element);
	const view = el('div', { class: 'wgrid' });
	const result = el('div', {});
	stage.append(view, result);

	function render() {
		const orders = [
			[1, 10],
			[3, 20],
			[9, 99]
		];
		if (state.duplicate) orders.splice(1, 0, [1, 5]);
		/** @type {(string|number|null)[][]} */
		const matched = [];
		for (const [id, name] of customers) {
			for (const order of orders) if (order[0] === id) matched.push([id, name, order[0], order[1]]);
		}
		const lonelyCustomers = customers
			.filter((customer) => !orders.some((order) => order[0] === customer[0]))
			.map((customer) => [customer[0], customer[1], null, null]);
		const lonelyOrders = orders
			.filter((order) => !customers.some((customer) => customer[0] === order[0]))
			.map((order) => [null, null, order[0], order[1]]);
		/** @type {Record<string, (string|number|null)[][]>} */
		const results = {
			inner: matched,
			left: [...matched, ...lonelyCustomers],
			right: [...matched, ...lonelyOrders],
			outer: [...matched, ...lonelyCustomers, ...lonelyOrders]
		};
		const merged = results[state.how];
		view.replaceChildren(
			el('div', {}, [
				el('div', { class: 'wcode' }, ['customers']),
				table(['id', 'name'], customers)
			]),
			el('div', {}, [
				el('div', { class: 'wcode' }, ['orders']),
				table(['customer_id', 'amount'], orders)
			])
		);
		result.replaceChildren(
			el('div', { class: 'wcode' }, [
				`customers.merge(orders, left_on="id", right_on="customer_id", how="${state.how}")`
			]),
			table(['id', 'name', 'customer_id', 'amount'], merged)
		);
		stats.update([
			{ label: 'rows out', value: merged.length },
			{
				label: 'unmatched customers',
				value: customers.filter((c) => !orders.some((o) => o[0] === c[0])).length
			},
			{
				label: 'orders with no customer',
				value: orders.filter((o) => !customers.some((c) => c[0] === o[0])).length
			}
		]);
	}
	render();
	return { shell };
}

// ---------------------------------------------------------------- pivot
/** @returns {Demo} */
function pivotMelt() {
	const sales = [
		['north', 'Q1', 5],
		['north', 'Q1', 7],
		['north', 'Q3', 3],
		['south', 'Q1', 20],
		['south', 'Q2', 10],
		['east', 'Q2', 8]
	];
	const regions = ['east', 'north', 'south'];
	const quarters = ['Q1', 'Q2', 'Q3'];
	const state = { aggfunc: 'sum', fill: false, long: false };
	const { shell, stage, controls, stats } = scaffold(
		'pivot',
		'Try it live',
		'North and Q1 appears twice (5 and 7): the aggregation function decides what that cell shows. The default is the mean.'
	);
	const aggfunc = createSelect('aggfunc', ['sum', 'mean', 'count', 'max'], 'sum', (value) => {
		state.aggfunc = value;
		render();
	});
	const fill = createToggle('fill_value=0', false, (value) => {
		state.fill = value;
		render();
	});
	const long = createToggle('melt the result back to long form', false, (value) => {
		state.long = value;
		render();
	});
	controls.append(aggfunc.element, fill.element, long.element, stats.element);
	const view = el('div', { class: 'wgrid' });
	stage.append(view);

	/** @param {number[]} values */
	const reduce = (values) => {
		if (state.aggfunc === 'sum') return values.reduce((a, b) => a + b, 0);
		if (state.aggfunc === 'count') return values.length;
		if (state.aggfunc === 'max') return Math.max(...values);
		return values.reduce((a, b) => a + b, 0) / values.length;
	};

	function render() {
		/** @type {(string|number|null)[][]} */
		const grid = regions.map((region) => [
			region,
			...quarters.map((quarter) => {
				const values = sales
					.filter((row) => row[0] === region && row[1] === quarter)
					.map((row) => /** @type {number} */ (row[2]));
				if (values.length === 0) return state.fill ? 0 : null;
				return Math.round(reduce(values) * 100) / 100;
			})
		]);
		const wide = table(['region', ...quarters], grid, (row) => (row[0] === 'north' ? 'sel' : ''));
		const longRows = grid.flatMap((row) =>
			quarters.map((quarter, i) => [row[0], quarter, row[i + 1]]).filter((r) => r[2] !== null)
		);
		view.replaceChildren(
			el('div', {}, [
				el('div', { class: 'wcode' }, ['sales  # one row per sale (long form)']),
				table(['region', 'quarter', 'revenue'], sales, (row) =>
					row[0] === 'north' && row[1] === 'Q1' ? 'sel' : ''
				)
			]),
			el('div', {}, [
				el('div', { class: 'wcode' }, [
					state.long
						? 'pivot.melt(id_vars="region", var_name="quarter", value_name="revenue")'
						: `sales.pivot_table(index="region", columns="quarter", values="revenue", aggfunc="${state.aggfunc}"${state.fill ? ', fill_value=0' : ''})`
				]),
				state.long ? table(['region', 'quarter', 'revenue'], longRows) : wide
			])
		);
		const cells = grid.flatMap((row) => row.slice(1));
		stats.update([
			{ label: 'north · Q1 shows', value: String(grid[1][1]) },
			{ label: 'empty cells', value: cells.filter((cell) => cell === null).length }
		]);
	}
	render();
	return { shell };
}

// ---------------------------------------------------------------- matplotlib object tree
/** @returns {Demo} */
function objectTree() {
	const parts = [
		{ id: 'figure', path: 'fig', note: 'the canvas: holds one or more Axes' },
		{ id: 'axes', path: 'fig.axes[0]', note: 'one plotting area with its own axes' },
		{ id: 'title', path: 'ax.title', note: 'ax.get_title() → "Revenue"' },
		{ id: 'xlabel', path: 'ax.xaxis.label', note: 'ax.get_xlabel() → "Month"' },
		{ id: 'ylabel', path: 'ax.yaxis.label', note: 'ax.get_ylabel() → "EUR"' },
		{ id: 'line0', path: 'ax.lines[0]', note: 'ax.lines[0].get_ydata() → [2, 4, 3, 6, 5]' },
		{ id: 'line1', path: 'ax.lines[1]', note: 'ax.lines[1].get_ydata() → [1, 3, 3, 4, 6]' },
		{ id: 'legend', path: 'ax.get_legend()', note: 'lists the labelled lines only' }
	];
	const state = { hover: '' };
	const { shell, stage, controls, stats } = scaffold(
		'object-tree',
		'Try it live',
		'Move over the chart (or click a name in the list): every visible thing is an object you can reach and read back.'
	);
	const list = el('div', { class: 'wtree' });
	controls.append(list, stats.element);
	/** @type {Record<string, [number, number, number, number]>} */
	let boxes = {};

	/** @param {string} id */
	const select = (id) => {
		state.hover = id;
		plot.redraw();
		renderList();
	};
	function renderList() {
		list.replaceChildren(
			...parts.map((part) => {
				const button = el(
					'button',
					{ type: 'button', class: `wtree-item${state.hover === part.id ? ' on' : ''}` },
					[part.path]
				);
				button.addEventListener('click', () => select(part.id));
				return button;
			})
		);
		const part = parts.find((p) => p.id === state.hover);
		stats.update(
			part
				? [
						{ label: 'object', value: part.path },
						{ label: 'what', value: part.note }
					]
				: [{ label: 'object', value: 'move over the chart' }]
		);
	}

	const plot = createCanvasPlot((ctx, width, height) => {
		const dark = getComputedStyle(shell).color;
		ctx.clearRect(0, 0, width, height);
		const fig = [8, 8, width - 16, height - 16];
		const ax = [56, 40, width - 80, height - 96];
		boxes = {
			figure: /** @type {[number, number, number, number]} */ (fig),
			axes: /** @type {[number, number, number, number]} */ (ax),
			title: [width / 2 - 40, 12, 80, 22],
			xlabel: [width / 2 - 28, height - 28, 56, 20],
			ylabel: [10, height / 2 - 28, 22, 56],
			line0: [ax[0], ax[1], ax[2], ax[3]],
			line1: [ax[0], ax[1], ax[2], ax[3]],
			legend: [ax[0] + ax[2] - 96, ax[1] + 8, 88, 40]
		};
		const mark = (/** @type {string} */ id) => {
			const b = boxes[id];
			if (!b || state.hover !== id) return;
			ctx.save();
			ctx.strokeStyle = '#f59e0b';
			ctx.fillStyle = 'rgba(245,158,11,0.12)';
			ctx.lineWidth = 2;
			ctx.fillRect(b[0], b[1], b[2], b[3]);
			ctx.strokeRect(b[0], b[1], b[2], b[3]);
			ctx.restore();
		};
		ctx.fillStyle = dark;
		ctx.strokeStyle = 'rgba(150,150,150,.8)';
		ctx.lineWidth = 1;
		ctx.strokeRect(ax[0], ax[1], ax[2], ax[3]);
		ctx.font = '600 13px sans-serif';
		ctx.textAlign = 'center';
		ctx.fillText('Revenue', width / 2, 28);
		ctx.font = '12px sans-serif';
		ctx.fillText('Month', width / 2, height - 12);
		ctx.save();
		ctx.translate(18, height / 2);
		ctx.rotate(-Math.PI / 2);
		ctx.fillText('EUR', 0, 0);
		ctx.restore();
		const series = [
			{ y: [2, 4, 3, 6, 5], colour: '#60a5fa' },
			{ y: [1, 3, 3, 4, 6], colour: '#f87171' }
		];
		series.forEach((s, k) => {
			ctx.strokeStyle = s.colour;
			ctx.lineWidth = 2;
			ctx.beginPath();
			s.y.forEach((value, i) => {
				const x = ax[0] + 14 + (i / 4) * (ax[2] - 28);
				const y = ax[1] + ax[3] - 10 - (value / 7) * (ax[3] - 20);
				if (i === 0) ctx.moveTo(x, y);
				else ctx.lineTo(x, y);
			});
			ctx.stroke();
			mark(`line${k}`);
		});
		ctx.fillStyle = dark;
		ctx.font = '11px sans-serif';
		ctx.textAlign = 'left';
		ctx.strokeStyle = '#60a5fa';
		ctx.beginPath();
		ctx.moveTo(boxes.legend[0] + 6, boxes.legend[1] + 12);
		ctx.lineTo(boxes.legend[0] + 24, boxes.legend[1] + 12);
		ctx.stroke();
		ctx.fillText('revenue', boxes.legend[0] + 30, boxes.legend[1] + 16);
		ctx.strokeStyle = '#f87171';
		ctx.beginPath();
		ctx.moveTo(boxes.legend[0] + 6, boxes.legend[1] + 28);
		ctx.lineTo(boxes.legend[0] + 24, boxes.legend[1] + 28);
		ctx.stroke();
		ctx.fillText('target', boxes.legend[0] + 30, boxes.legend[1] + 32);
		for (const id of ['figure', 'axes', 'title', 'xlabel', 'ylabel', 'legend']) mark(id);
	});
	plot.element.addEventListener('mousemove', (event) => {
		const rect = plot.element.getBoundingClientRect();
		const x = event.clientX - rect.left;
		const y = event.clientY - rect.top;
		const order = ['legend', 'title', 'xlabel', 'ylabel', 'line0', 'axes', 'figure'];
		const hit = order.find((id) => {
			const b = boxes[id];
			return b && x >= b[0] && x <= b[0] + b[2] && y >= b[1] && y <= b[1] + b[3];
		});
		if (hit && hit !== state.hover) select(hit);
	});
	stage.append(plot.element);
	renderList();
	return { shell, destroy: plot.destroy };
}

// ---------------------------------------------------------------- colour scales
/** @returns {Demo} */
function colourScale() {
	const strong = [
		[1, 0.9, -0.7, 0.1, 0.3],
		[0.9, 1, -0.6, 0.0, 0.2],
		[-0.7, -0.6, 1, 0.2, -0.1],
		[0.1, 0.0, 0.2, 1, 0.8],
		[0.3, 0.2, -0.1, 0.8, 1]
	];
	const weak = [
		[1, 0.3, 0.1, -0.2, 0.0],
		[0.3, 1, 0.2, 0.1, -0.1],
		[0.1, 0.2, 1, 0.25, 0.05],
		[-0.2, 0.1, 0.25, 1, 0.1],
		[0.0, -0.1, 0.05, 0.1, 1]
	];
	const state = { pinned: false, zmin: -1, zmax: 1 };
	const { shell, stage, controls, stats } = scaffold(
		'colour-scale',
		'Try it live',
		'With an automatic range the weak matrix (largest link 0.3) is painted as vividly as the strong one. Pinning the scale to −1…1 makes the colours mean the same thing in both.'
	);
	const pin = createToggle('pin the colour scale to the range below', false, (value) => {
		state.pinned = value;
		draw();
	});
	const zmin = createSlider({ label: 'zmin', min: -1, max: 0, step: 0.1, value: -1 });
	const zmax = createSlider({ label: 'zmax', min: 0, max: 1, step: 0.1, value: 1 });
	for (const slider of [zmin, zmax]) {
		slider.input.addEventListener('input', () => {
			state.zmin = Number(zmin.input.value);
			state.zmax = Number(zmax.input.value);
			draw();
		});
	}
	controls.append(pin.element, zmin.element, zmax.element, stats.element);

	/** @param {number} t in 0..1, diverging blue-white-red */
	const colour = (t) => {
		const x = Math.min(1, Math.max(0, t));
		const [r, g, b] =
			x < 0.5
				? [40 + x * 2 * 215, 90 + x * 2 * 165, 210 + x * 2 * 45]
				: [255, 255 - (x - 0.5) * 2 * 175, 255 - (x - 0.5) * 2 * 215];
		return `rgb(${Math.round(r)},${Math.round(g)},${Math.round(b)})`;
	};
	const plot = createCanvasPlot((ctx, width, height) => {
		ctx.clearRect(0, 0, width, height);
		const half = width / 2;
		const size = Math.min(half - 24, height - 40) / 5;
		[
			{ m: strong, left: 12, name: 'strong' },
			{ m: weak, left: half + 12, name: 'weak' }
		].forEach(({ m, left, name }) => {
			const flat = m.flat();
			const lo = state.pinned ? state.zmin : Math.min(...flat);
			const hi = state.pinned ? state.zmax : Math.max(...flat);
			ctx.fillStyle = getComputedStyle(shell).color;
			ctx.font = '12px sans-serif';
			ctx.textAlign = 'left';
			ctx.fillText(`${name}: colours span ${lo.toFixed(1)} … ${hi.toFixed(1)}`, left, 16);
			m.forEach((row, i) =>
				row.forEach((value, j) => {
					ctx.fillStyle = colour(hi === lo ? 0.5 : (value - lo) / (hi - lo));
					ctx.fillRect(left + j * size, 26 + i * size, size - 2, size - 2);
					ctx.fillStyle = '#111';
					ctx.font = '10px sans-serif';
					ctx.textAlign = 'center';
					ctx.fillText(
						value.toFixed(1),
						left + j * size + size / 2 - 1,
						26 + i * size + size / 2 + 3
					);
				})
			);
		});
	});
	/** @param {number[][]} m */
	const offDiagonalMax = (m) =>
		Math.max(...m.flatMap((row, i) => row.filter((_, j) => i !== j)).map(Math.abs));
	function draw() {
		stats.update([
			{ label: 'strongest link (left)', value: offDiagonalMax(strong).toFixed(1) },
			{ label: 'strongest link (right)', value: offDiagonalMax(weak).toFixed(1) },
			{
				label: 'scale',
				value: state.pinned
					? `pinned ${state.zmin.toFixed(1)} … ${state.zmax.toFixed(1)}`
					: 'automatic (min … max of each)'
			}
		]);
		plot.redraw();
	}
	stage.append(plot.element);
	draw();
	return { shell, destroy: plot.destroy };
}

// ---------------------------------------------------------------- histogram + KDE
/** @returns {Demo} */
function binsAndBandwidth() {
	const random = seededRandom(42);
	const normal = () => Math.sqrt(-2 * Math.log(1 - random())) * Math.cos(2 * Math.PI * random());
	const sample = Array.from({ length: 70 }, (_, i) =>
		i % 3 === 0 ? 4 + 0.8 * normal() : 0.5 * normal()
	);
	const n = sample.length;
	const mean = sample.reduce((a, b) => a + b, 0) / n;
	const sd = Math.sqrt(sample.reduce((a, b) => a + (b - mean) ** 2, 0) / n);
	const scott = 1.06 * sd * n ** (-1 / 5);
	const lo = Math.min(...sample);
	const hi = Math.max(...sample);
	const state = { bins: 10, bandwidth: Math.round(scott * 100) / 100, view: 'histogram + KDE' };
	const { shell, stage, controls, stats } = scaffold(
		'bins-bandwidth',
		'Try it live',
		'Too few bins hide the second hump; too many draw noise. The KDE bandwidth does the same job for the smooth curve.'
	);
	const bins = createSlider({ label: 'bins', min: 2, max: 40, step: 1, value: state.bins });
	const bandwidth = createSlider({
		label: 'KDE bandwidth',
		min: 0.1,
		max: 2,
		step: 0.05,
		value: state.bandwidth
	});
	const view = createSelect('view', ['histogram + KDE', 'ECDF'], 'histogram + KDE', (value) => {
		state.view = value;
		redraw();
	});
	const scottButton = createActionButton("Use Scott's rule", {
		onClick: () => {
			bandwidth.input.value = String(Math.round(scott * 100) / 100);
			bandwidth.input.dispatchEvent(new Event('input'));
		}
	});
	bins.input.addEventListener('input', () => {
		state.bins = Number(bins.input.value);
		redraw();
	});
	bandwidth.input.addEventListener('input', () => {
		state.bandwidth = Number(bandwidth.input.value);
		redraw();
	});
	controls.append(bins.element, bandwidth.element, view.element, scottButton, stats.element);

	const plot = createCanvasPlot((ctx, width, height) => {
		ctx.clearRect(0, 0, width, height);
		const pad = { l: 36, r: 10, t: 14, b: 26 };
		const w = width - pad.l - pad.r;
		const h = height - pad.t - pad.b;
		const x0 = lo - 1;
		const x1 = hi + 1;
		const px = (/** @type {number} */ x) => pad.l + ((x - x0) / (x1 - x0)) * w;
		ctx.fillStyle = getComputedStyle(shell).color;
		ctx.strokeStyle = 'rgba(150,150,150,.7)';
		ctx.font = '11px sans-serif';
		ctx.beginPath();
		ctx.moveTo(pad.l, pad.t + h);
		ctx.lineTo(pad.l + w, pad.t + h);
		ctx.stroke();
		if (state.view === 'ECDF') {
			const sorted = [...sample].sort((a, b) => a - b);
			ctx.strokeStyle = '#34d399';
			ctx.lineWidth = 2;
			ctx.beginPath();
			ctx.moveTo(px(x0), pad.t + h);
			sorted.forEach((value, i) => {
				ctx.lineTo(px(value), pad.t + h - (i / n) * h);
				ctx.lineTo(px(value), pad.t + h - ((i + 1) / n) * h);
			});
			ctx.lineTo(px(x1), pad.t);
			ctx.stroke();
			ctx.fillText('fraction of data at or below x', pad.l + 6, pad.t + 10);
			return;
		}
		const width_ = (hi - lo) / state.bins;
		const counts = Array(state.bins).fill(0);
		for (const value of sample)
			counts[Math.min(state.bins - 1, Math.floor((value - lo) / width_))]++;
		const density = counts.map((c) => c / (n * width_));
		const kde = (/** @type {number} */ x) =>
			sample.reduce((sum, v) => sum + Math.exp(-0.5 * ((x - v) / state.bandwidth) ** 2), 0) /
			(n * state.bandwidth * Math.sqrt(2 * Math.PI));
		const curve = Array.from({ length: 160 }, (_, i) => x0 + ((x1 - x0) * i) / 159).map((x) => [
			x,
			kde(x)
		]);
		const top = Math.max(...density, ...curve.map((p) => p[1])) * 1.1;
		const py = (/** @type {number} */ d) => pad.t + h - (d / top) * h;
		ctx.fillStyle = 'rgba(96,165,250,.55)';
		density.forEach((d, i) => {
			const left = px(lo + i * width_);
			ctx.fillRect(left, py(d), px(lo + (i + 1) * width_) - left - 1, pad.t + h - py(d));
		});
		ctx.strokeStyle = '#f59e0b';
		ctx.lineWidth = 2;
		ctx.beginPath();
		curve.forEach(([x, d], i) => (i === 0 ? ctx.moveTo(px(x), py(d)) : ctx.lineTo(px(x), py(d))));
		ctx.stroke();
		ctx.fillStyle = 'rgba(150,150,150,.9)';
		for (const value of sample) ctx.fillRect(px(value) - 0.5, pad.t + h + 3, 1, 6);
	});
	function redraw() {
		const binWidth = (hi - lo) / state.bins;
		stats.update([
			{ label: 'bin width', value: binWidth.toFixed(2) },
			{ label: 'bandwidth', value: state.bandwidth.toFixed(2) },
			{ label: "Scott's rule", value: scott.toFixed(2) },
			{ label: 'Sturges bins', value: String(Math.ceil(Math.log2(n)) + 1) }
		]);
		plot.redraw();
	}
	stage.append(plot.element);
	redraw();
	return { shell, destroy: plot.destroy };
}

// ---------------------------------------------------------------- animation frames
/** @returns {Demo} */
function animationFrames() {
	const frames = [
		{
			name: '2000',
			points: [
				[1, 50],
				[2, 60],
				[3, 70],
				[1.5, 55]
			]
		},
		{
			name: '2010',
			points: [
				[1.5, 55],
				[2.5, 62],
				[4.5, 75],
				[2, 58]
			]
		},
		{
			name: '2020',
			points: [
				[2, 58],
				[3.5, 66],
				[6, 80],
				[2.5, 62]
			]
		}
	];
	const all = frames.flatMap((f) => f.points);
	const fixed = {
		x: [Math.min(...all.map((p) => p[0])), Math.max(...all.map((p) => p[0]))],
		y: [Math.min(...all.map((p) => p[1])), Math.max(...all.map((p) => p[1]))]
	};
	const state = { frame: 0, fixed: true };
	const { shell, stage, controls, stats } = scaffold(
		'animation-frames',
		'Try it live',
		'With autoscaling each frame is stretched to fill the box, so the points seem to stand still while the ruler moves. Fixed ranges show the real growth.'
	);
	const slider = createSlider({
		label: 'frame',
		min: 0,
		max: frames.length - 1,
		step: 1,
		value: 0
	});
	slider.input.addEventListener('input', () => {
		state.frame = Number(slider.input.value);
		redraw();
	});
	const toggle = createToggle('fix the axis ranges (range_x, range_y)', true, (value) => {
		state.fixed = value;
		redraw();
	});
	/** @type {ReturnType<typeof setInterval> | null} */
	let timer = null;
	const play = createActionButton('Play', {
		primary: true,
		onClick: () => {
			if (timer) {
				clearInterval(timer);
				timer = null;
				play.textContent = 'Play';
				return;
			}
			play.textContent = 'Pause';
			timer = setInterval(() => {
				state.frame = (state.frame + 1) % frames.length;
				slider.input.value = String(state.frame);
				slider.update();
				redraw();
			}, 800);
		}
	});
	controls.append(slider.element, toggle.element, play, stats.element);

	const plot = createCanvasPlot((ctx, width, height) => {
		ctx.clearRect(0, 0, width, height);
		const pad = { l: 40, r: 14, t: 14, b: 28 };
		const w = width - pad.l - pad.r;
		const h = height - pad.t - pad.b;
		const points = frames[state.frame].points;
		const xs = state.fixed
			? fixed.x
			: [Math.min(...points.map((p) => p[0])), Math.max(...points.map((p) => p[0]))];
		const ys = state.fixed
			? fixed.y
			: [Math.min(...points.map((p) => p[1])), Math.max(...points.map((p) => p[1]))];
		const padRange = (/** @type {number[]} */ r) => [
			r[0] - (r[1] - r[0]) * 0.1,
			r[1] + (r[1] - r[0]) * 0.1
		];
		const [xa, xb] = padRange(xs);
		const [ya, yb] = padRange(ys);
		const px = (/** @type {number} */ v) => pad.l + ((v - xa) / (xb - xa)) * w;
		const py = (/** @type {number} */ v) => pad.t + h - ((v - ya) / (yb - ya)) * h;
		ctx.strokeStyle = 'rgba(150,150,150,.7)';
		ctx.fillStyle = getComputedStyle(shell).color;
		ctx.font = '11px sans-serif';
		ctx.strokeRect(pad.l, pad.t, w, h);
		ctx.textAlign = 'right';
		for (const t of [ya + (yb - ya) * 0.1, (ya + yb) / 2, yb - (yb - ya) * 0.1])
			ctx.fillText(t.toFixed(0), pad.l - 4, py(t) + 4);
		ctx.textAlign = 'center';
		for (const t of [xa + (xb - xa) * 0.1, (xa + xb) / 2, xb - (xb - xa) * 0.1])
			ctx.fillText(t.toFixed(1), px(t), pad.t + h + 14);
		points.forEach(([x, y], i) => {
			ctx.fillStyle = GROUP_COLOURS[i % GROUP_COLOURS.length];
			ctx.beginPath();
			ctx.arc(px(x), py(y), 7, 0, Math.PI * 2);
			ctx.fill();
		});
		ctx.fillStyle = getComputedStyle(shell).color;
		ctx.textAlign = 'left';
		ctx.font = '600 13px sans-serif';
		ctx.fillText(frames[state.frame].name, pad.l + 8, pad.t + 18);
	});
	function redraw() {
		const points = frames[state.frame].points;
		const xs = state.fixed
			? fixed.x
			: [Math.min(...points.map((p) => p[0])), Math.max(...points.map((p) => p[0]))];
		stats.update([
			{ label: 'frame', value: frames[state.frame].name },
			{ label: 'x range', value: `${xs[0].toFixed(1)} … ${xs[1].toFixed(1)}` },
			{ label: 'axes', value: state.fixed ? 'fixed for all frames' : 'rescaled every frame' }
		]);
		plot.redraw();
	}
	stage.append(plot.element);
	redraw();
	return {
		shell,
		destroy: () => {
			if (timer) clearInterval(timer);
			plot.destroy();
		}
	};
}

const demos = {
	'data-science-pandas-label-vs-position': labelVsPosition,
	'data-science-pandas-groupby-aggregate': groupBySplitApply,
	'data-science-pandas-merge-join': joinTypes,
	'data-science-pandas-pivot-crosstab': pivotMelt,
	'data-science-matplotlib-figure-axes-lines': objectTree,
	'data-science-seaborn-heatmaps-correlation': colourScale,
	'data-science-seaborn-distribution-plots': binsAndBandwidth,
	'data-science-plotly-animation-frames': animationFrames
};

/** @param {HTMLElement} root */
export function mount(root) {
	const id = root.dataset.widget ?? '';
	if (!dataToolsVisualizerIds.includes(id) || !(id in demos)) return () => {};
	const demo = demos[/** @type {keyof typeof demos} */ (id)]();
	// The base .tt-widget is a two-column grid (canvas + controls); this one lays itself out.
	root.classList.add('tt-widget', 'tt-data-widget');
	root.replaceChildren(demo.shell);
	return () => {
		demo.destroy?.();
		root.replaceChildren();
	};
}
