/** @param {{ label: string; min: number; max: number; step?: number; value: number }} options */
export function createSlider({ label, min, max, step = 1, value }) {
	const wrapper = document.createElement('div');
	wrapper.className = 'ctrl';
	const labelElement = document.createElement('label');
	const name = document.createElement('span');
	name.textContent = label;
	const output = document.createElement('b');
	labelElement.append(name, output);

	const input = document.createElement('input');
	input.type = 'range';
	input.min = String(min);
	input.max = String(max);
	input.step = String(step);
	input.value = String(value);
	input.setAttribute('aria-label', label);
	const update = () => {
		const digits = String(step).includes('.') ? String(step).split('.')[1].length : 0;
		output.textContent = Number(input.value).toFixed(digits);
	};
	input.addEventListener('input', update);
	update();
	wrapper.append(labelElement, input);
	return { element: wrapper, input, update };
}
