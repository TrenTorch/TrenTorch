// Colour themes for the IDE, in the spirit of VS Code's: pick one and the whole
// workbench (guide, results, editor and its syntax colours) changes together.
// A theme is plain data. `ui` becomes CSS variables on the IDE shell, `editor`
// feeds the CodeMirror theme in CodeEditor.svelte.

export type IdeEditorPalette = {
	bg: string;
	fg: string;
	caret: string;
	selection: string;
	activeLine: string;
	gutter: string;
	comment: string;
	keyword: string;
	operator: string;
	fn: string;
	cls: string;
	string: string;
	number: string;
	property: string;
	variable: string;
	meta: string;
	invalid: string;
};

export type IdeTheme = {
	id: string;
	name: string;
	/** One line shown under the name in the picker. */
	blurb: string;
	mode: 'dark' | 'light';
	ui: {
		gutter: string;
		panel: string;
		head: string;
		line: string;
		chip: string;
		text: string;
		text2: string;
		code: string;
		accent: string;
		accentFg: string;
		ok: string;
		okFg: string;
		bad: string;
		warn: string;
	};
	editor: IdeEditorPalette;
};

export const IDE_THEMES: IdeTheme[] = [
	{
		id: 'ember',
		name: 'Ember',
		blurb: 'Warm dark. The default.',
		mode: 'dark',
		ui: {
			gutter: '#0d0c0b',
			panel: '#171513',
			head: '#1e1b18',
			line: '#2f2a25',
			chip: '#28231f',
			text: '#f2ede6',
			text2: '#a99f93',
			code: '#12100e',
			accent: '#e0795a',
			accentFg: '#1b0b04',
			ok: '#5fd39a',
			okFg: '#06180d',
			bad: '#e5786f',
			warn: '#ffb04a'
		},
		editor: {
			bg: '#12100e',
			fg: '#f2ede6',
			caret: '#e0795a',
			selection: '#e0795a33',
			activeLine: '#ffffff0a',
			gutter: '#6f665b',
			comment: '#8a7f72',
			keyword: '#ff7b5c',
			operator: '#ff9a7a',
			fn: '#ffc27a',
			cls: '#f5d27a',
			string: '#b5d98b',
			number: '#ffb454',
			property: '#e6b673',
			variable: '#f2ede6',
			meta: '#d7a8ff',
			invalid: '#e5786f'
		}
	},
	{
		id: 'midnight',
		name: 'Midnight',
		blurb: 'Deep blue dark.',
		mode: 'dark',
		ui: {
			gutter: '#070a12',
			panel: '#0f1522',
			head: '#141c2d',
			line: '#232e47',
			chip: '#1b2540',
			text: '#e6ecfa',
			text2: '#8c9bbd',
			code: '#0a0f1b',
			accent: '#5aa2ff',
			accentFg: '#04101f',
			ok: '#4fd8a4',
			okFg: '#05170f',
			bad: '#e87b8b',
			warn: '#ffcb6b'
		},
		editor: {
			bg: '#0a0f1b',
			fg: '#d6deeb',
			caret: '#5aa2ff',
			selection: '#5aa2ff33',
			activeLine: '#ffffff0a',
			gutter: '#4b5a7e',
			comment: '#5c6b8f',
			keyword: '#c792ea',
			operator: '#89ddff',
			fn: '#82aaff',
			cls: '#ffcb6b',
			string: '#c3e88d',
			number: '#f78c6c',
			property: '#82aaff',
			variable: '#d6deeb',
			meta: '#c792ea',
			invalid: '#e87b8b'
		}
	},
	{
		id: 'dracula',
		name: 'Dracula',
		blurb: 'Purple on charcoal.',
		mode: 'dark',
		ui: {
			gutter: '#14151c',
			panel: '#1e1f29',
			head: '#252633',
			line: '#343746',
			chip: '#2c2e3d',
			text: '#f8f8f2',
			text2: '#a0a3bd',
			code: '#181920',
			accent: '#bd93f9',
			accentFg: '#1b1230',
			ok: '#50fa7b',
			okFg: '#06200f',
			bad: '#ff5555',
			warn: '#f1fa8c'
		},
		editor: {
			bg: '#181920',
			fg: '#f8f8f2',
			caret: '#f8f8f2',
			selection: '#bd93f933',
			activeLine: '#ffffff0a',
			gutter: '#5b5f7a',
			comment: '#6272a4',
			keyword: '#ff79c6',
			operator: '#ff79c6',
			fn: '#50fa7b',
			cls: '#8be9fd',
			string: '#f1fa8c',
			number: '#bd93f9',
			property: '#66d9ef',
			variable: '#f8f8f2',
			meta: '#ffb86c',
			invalid: '#ff5555'
		}
	},
	{
		id: 'nord',
		name: 'Nord',
		blurb: 'Muted blue-grey dark.',
		mode: 'dark',
		ui: {
			gutter: '#242933',
			panel: '#2e3440',
			head: '#353c4a',
			line: '#434c5e',
			chip: '#3b4252',
			text: '#eceff4',
			text2: '#a3adc2',
			code: '#272c36',
			accent: '#88c0d0',
			accentFg: '#1b2430',
			ok: '#a3be8c',
			okFg: '#14200c',
			bad: '#bf616a',
			warn: '#ebcb8b'
		},
		editor: {
			bg: '#272c36',
			fg: '#d8dee9',
			caret: '#88c0d0',
			selection: '#88c0d033',
			activeLine: '#ffffff0a',
			gutter: '#616e88',
			comment: '#616e88',
			keyword: '#81a1c1',
			operator: '#81a1c1',
			fn: '#88c0d0',
			cls: '#8fbcbb',
			string: '#a3be8c',
			number: '#b48ead',
			property: '#88c0d0',
			variable: '#d8dee9',
			meta: '#d08770',
			invalid: '#bf616a'
		}
	},
	{
		id: 'paper',
		name: 'Paper',
		blurb: 'Warm off-white light.',
		mode: 'light',
		ui: {
			gutter: '#e9e5da',
			panel: '#fbf9f4',
			head: '#f2eee4',
			line: '#ddd6c6',
			chip: '#ebe5d6',
			text: '#1f1c17',
			text2: '#6b6558',
			code: '#f6f2e8',
			accent: '#d9480f',
			accentFg: '#ffffff',
			ok: '#1f7a4d',
			okFg: '#ffffff',
			bad: '#c92a2a',
			warn: '#b8590a'
		},
		editor: {
			bg: '#f6f2e8',
			fg: '#1f1c17',
			caret: '#d9480f',
			selection: '#d9480f2b',
			activeLine: '#00000009',
			gutter: '#a39a86',
			comment: '#8a8272',
			keyword: '#b4351c',
			operator: '#b4351c',
			fn: '#5b3fb5',
			cls: '#8a5a00',
			string: '#1f6f43',
			number: '#0b5fa5',
			property: '#0b5fa5',
			variable: '#1f1c17',
			meta: '#7a3fb0',
			invalid: '#a61e1e'
		}
	}
];

export const DEFAULT_DARK_THEME = 'ember';
export const DEFAULT_LIGHT_THEME = 'paper';

export function getTheme(id: string | null | undefined): IdeTheme | undefined {
	return IDE_THEMES.find((theme) => theme.id === id);
}

/** CSS variables for the IDE shell. The first block is the theme's own tokens;
 * the second re-points the site's tokens (--background, --border ...) so every
 * component inside the shell picks the theme up without changing its classes. */
export function themeStyle(theme: IdeTheme): string {
	const u = theme.ui;
	const vars: Record<string, string> = {
		'--ide-gutter': u.gutter,
		'--ide-panel': u.panel,
		'--ide-head': u.head,
		'--ide-line': u.line,
		'--ide-chip': u.chip,
		'--ide-text': u.text,
		'--ide-text-2': u.text2,
		'--ide-code': u.code,
		'--ide-accent': u.accent,
		'--ide-accent-fg': u.accentFg,
		'--ide-ok': u.ok,
		'--ide-ok-fg': u.okFg,
		'--ide-bad': u.bad,
		'--ide-warn': u.warn,
		'--syn-fg': theme.editor.fg,
		'--syn-comment': theme.editor.comment,
		'--syn-keyword': theme.editor.keyword,
		'--syn-operator': theme.editor.operator,
		'--syn-fn': theme.editor.fn,
		'--syn-cls': theme.editor.cls,
		'--syn-string': theme.editor.string,
		'--syn-number': theme.editor.number,
		'--syn-property': theme.editor.property,
		'--syn-variable': theme.editor.variable,
		'--syn-meta': theme.editor.meta,
		'--syn-invalid': theme.editor.invalid,
		'color-scheme': theme.mode
	};
	return Object.entries(vars)
		.map(([key, value]) => `${key}:${value}`)
		.join(';');
}
