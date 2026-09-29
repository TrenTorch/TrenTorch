/** @param {string} label @param {{ primary?: boolean; onClick?: () => void }} [options] */
export function createActionButton(label, { primary = false, onClick } = {}) {
	const button = document.createElement('button');
	button.type = 'button';
	button.className = `wbtn${primary ? ' primary' : ''}`;
	button.textContent = label;
	if (onClick) button.addEventListener('click', onClick);
	return button;
}
