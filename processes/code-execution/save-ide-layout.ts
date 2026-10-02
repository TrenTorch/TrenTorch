import { LAYOUT_KEY, type IdeLayout } from './ide-layout-key';

export function saveIdeLayout(layout: IdeLayout): void {
	if (typeof window === 'undefined') return;
	try {
		localStorage.setItem(LAYOUT_KEY, JSON.stringify(layout));
	} catch (e) {
		console.error('Failed to save IDE layout', e);
	}
}
