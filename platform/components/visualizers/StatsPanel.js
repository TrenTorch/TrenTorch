export function createStatsPanel() {
	const panel = document.createElement('div');
	panel.className = 'readout';

	return {
		element: panel,
		/** @param {{ label: string; value: string | number }[]} rows */
		update(rows) {
			panel.replaceChildren(
				...rows.map(({ label, value }) => {
					const row = document.createElement('div');
					const name = document.createElement('span');
					name.textContent = label;
					const result = document.createElement('b');
					result.textContent = String(value);
					row.append(name, result);
					return row;
				})
			);
		}
	};
}
