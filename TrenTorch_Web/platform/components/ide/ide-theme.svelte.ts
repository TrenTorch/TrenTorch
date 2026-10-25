import { browser } from '$app/environment';
import {
	DEFAULT_DARK_THEME,
	DEFAULT_LIGHT_THEME,
	IDE_THEMES,
	getTheme,
	type IdeTheme
} from './ide-themes';

const STORAGE_KEY = 'trentorch-ide-theme';

// The chosen IDE theme, remembered in this browser. A first-time visitor gets
// Ember on a dark site and Paper on a light one; after that their pick wins.
class IdeThemeState {
	id = $state(DEFAULT_DARK_THEME);
	current = $derived<IdeTheme>(getTheme(this.id) ?? IDE_THEMES[0]);

	init() {
		if (!browser) return;
		try {
			const saved = getTheme(localStorage.getItem(STORAGE_KEY));
			if (saved) {
				this.id = saved.id;
				return;
			}
		} catch {
			// storage blocked: fall through to the site's mode
		}
		this.id = document.documentElement.classList.contains('dark')
			? DEFAULT_DARK_THEME
			: DEFAULT_LIGHT_THEME;
	}

	set(id: string) {
		if (!getTheme(id)) return;
		this.id = id;
		try {
			localStorage.setItem(STORAGE_KEY, id);
		} catch {
			// not remembered, still applied for this visit
		}
	}
}

export const ideTheme = new IdeThemeState();
