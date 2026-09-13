import { LAYOUT_KEY, type IdeLayout } from './ide-layout-key';

export function loadIdeLayout(defaults: IdeLayout): IdeLayout {
	if (typeof window === 'undefined') return defaults;
	try {
		const raw = localStorage.getItem(LAYOUT_KEY);
		if (!raw) return defaults;
		const parsed = JSON.parse(raw);
		return {
			leftPanePercent:
				typeof parsed.leftPanePercent === 'number'
					? parsed.leftPanePercent
					: defaults.leftPanePercent,
			bottomPanePercent:
				typeof parsed.bottomPanePercent === 'number'
					? parsed.bottomPanePercent
					: defaults.bottomPanePercent
		};
	} catch (e) {
		console.error('Failed to load IDE layout', e);
		return defaults;
	}
}
