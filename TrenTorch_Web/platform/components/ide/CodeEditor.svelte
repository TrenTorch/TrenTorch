<script lang="ts" module>
	export const EDITOR_FONT_MIN = 10;
	export const EDITOR_FONT_MAX = 32;
	export const EDITOR_FONT_DEFAULT = 14;
</script>

<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import type { EditorView as EditorViewType } from '@codemirror/view';
	import { IDE_THEMES, type IdeEditorPalette } from './ide-themes';

	// CodeMirror (~1 MB of source across @codemirror/*) loads via a dynamic
	// import inside onMount, never a static import: it is a client-only
	// editor, and a static import drags the whole thing into the SSR /
	// serverless bundle where it is dead weight that also slows cold starts.
	/* eslint-disable @typescript-eslint/no-explicit-any */

	let {
		value = $bindable(''),
		onRun = () => {},
		onChange = () => {},
		onCursorChange = () => {},
		// eslint-disable-next-line no-useless-assignment -- placeholder replaced by rebuildEditor() once CodeMirror loads
		reindent = $bindable<() => void>(() => {}),
		language = 'python',
		fontSize = $bindable(EDITOR_FONT_DEFAULT),
		palette = IDE_THEMES[0].editor,
		dark = true
	} = $props<{
		value: string;
		onRun?: (val?: void) => void;
		onChange?: (val: string) => void;
		onCursorChange?: (pos: { line: number; col: number }) => void;
		reindent?: () => void;
		language?: 'python' | 'sql';
		fontSize?: number;
		/** Editor and syntax colours of the chosen IDE theme (see ide-themes.ts). */
		palette?: IdeEditorPalette;
		dark?: boolean;
	}>();

	let editorContainer: HTMLDivElement;
	let editorView: EditorViewType | null = null;

	// Populated once CodeMirror has loaded. Everything that touches these
	// runs after loadCm() resolves, so nothing here executes at module eval.
	let cm: {
		EditorView: any;
		EditorState: any;
		basicSetup: any;
		indentUnit: any;
		indentMore: any;
		indentLess: any;
		indentRange: any;
		python: any;
		sql: any;
		sqlite: any;
		keymap: any;
		HighlightStyle: any;
		syntaxHighlighting: any;
		tags: any;
	} | null = null;
	// Plain style spec for the chosen palette; turned into a real EditorView.theme
	// extension once CodeMirror has loaded.
	function themeSpec(p: IdeEditorPalette) {
		return {
			'&': {
				height: '100%',
				fontFamily: "'IBM Plex Mono', 'Geist Mono', ui-monospace, Menlo, monospace",
				fontSize: 'var(--editor-font-size)',
				backgroundColor: p.bg,
				color: p.fg
			},
			'.cm-content': { padding: '12px 0', caretColor: p.caret },
			'.cm-cursor, .cm-dropCursor': { borderLeftColor: p.caret, borderLeftWidth: '2px' },
			'&.cm-focused .cm-selectionBackground, .cm-selectionBackground, .cm-content ::selection': {
				backgroundColor: p.selection + ' !important'
			},
			'.cm-gutters': {
				backgroundColor: p.bg,
				color: p.gutter,
				borderRight: '1px solid transparent',
				paddingRight: '6px'
			},
			'.cm-activeLineGutter': { backgroundColor: p.activeLine, color: p.fg },
			'.cm-activeLine': { backgroundColor: p.activeLine },
			'.cm-line': { padding: '0 12px' },
			'.cm-scroller': { overflow: 'auto', lineHeight: '1.65' },
			'.cm-matchingBracket, .cm-nonmatchingBracket': {
				backgroundColor: p.selection,
				outline: 'none'
			}
		};
	}

	// Syntax token colours of the chosen palette.
	function highlightSpec(t: any, p: IdeEditorPalette) {
		return [
			{ tag: t.comment, color: p.comment, fontStyle: 'italic' },
			{
				tag: [t.keyword, t.controlKeyword, t.moduleKeyword, t.operatorKeyword],
				color: p.keyword
			},
			{ tag: [t.definitionKeyword, t.self], color: p.keyword },
			{
				tag: [t.function(t.variableName), t.function(t.definition(t.variableName))],
				color: p.fn
			},
			{ tag: [t.className, t.definition(t.className), t.typeName], color: p.cls },
			{ tag: [t.string, t.special(t.string), t.docString], color: p.string },
			{ tag: [t.number, t.bool, t.null], color: p.number },
			{ tag: t.operator, color: p.operator },
			{ tag: t.punctuation, color: p.fg },
			{ tag: t.propertyName, color: p.property },
			{ tag: [t.variableName, t.definition(t.variableName)], color: p.variable },
			{ tag: t.meta, color: p.meta },
			{ tag: t.invalid, color: p.invalid }
		];
	}

	async function loadCm() {
		const [cmMod, stateMod, pyMod, sqlMod, viewMod, langMod, highlightMod, commandsMod] =
			await Promise.all([
				import('codemirror'),
				import('@codemirror/state'),
				import('@codemirror/lang-python'),
				import('@codemirror/lang-sql'),
				import('@codemirror/view'),
				import('@codemirror/language'),
				import('@lezer/highlight'),
				import('@codemirror/commands')
			]);
		cm = {
			EditorView: cmMod.EditorView,
			basicSetup: cmMod.basicSetup,
			indentUnit: langMod.indentUnit,
			indentMore: commandsMod.indentMore,
			indentLess: commandsMod.indentLess,
			indentRange: langMod.indentRange,
			EditorState: stateMod.EditorState,
			python: pyMod.python,
			sql: sqlMod.sql,
			sqlite: sqlMod.SQLite,
			keymap: viewMod.keymap,
			HighlightStyle: langMod.HighlightStyle,
			syntaxHighlighting: langMod.syntaxHighlighting,
			tags: highlightMod.tags
		};
	}

	function zoomEditor(delta: number) {
		fontSize = Math.min(EDITOR_FONT_MAX, Math.max(EDITOR_FONT_MIN, fontSize + delta));
	}

	function rebuildEditor(doc: string) {
		if (!cm) return;
		editorView?.destroy();

		const insertIndent = (view: any) => {
			const state = view.state;
			if (state.selection.ranges.some((range: any) => !range.empty))
				return cm?.indentMore(view) ?? false;
			const size = language === 'sql' ? 2 : 4;
			const head = state.selection.main.head;
			const column = head - state.doc.lineAt(head).from;
			view.dispatch(state.replaceSelection(' '.repeat(size - (column % size))));
			return true;
		};

		const runKeyBinding = cm.keymap.of([
			{ key: 'Mod-Enter', run: () => (onRun(), true) },
			{ key: 'Shift-Enter', run: () => (onRun(), true) },
			{ key: 'Mod-=', run: () => (zoomEditor(1), true) },
			{ key: 'Mod-+', run: () => (zoomEditor(1), true) },
			{ key: 'Mod--', run: () => (zoomEditor(-1), true) },
			{ key: 'Mod-0', run: () => ((fontSize = EDITOR_FONT_DEFAULT), true) },
			// Tab types spaces up to the next indent stop at the cursor and only re-indents whole
			// lines when text is selected; Shift-Tab takes an indent back. (indentWithTab moved
			// the whole line, and insertTab types a tab character, which Python dislikes.)
			{ key: 'Tab', run: insertIndent, shift: cm.indentLess }
		]);

		const updateListener = cm.EditorView.updateListener.of((update: any) => {
			if (update.docChanged) {
				const newValue = update.state.doc.toString();
				value = newValue;
				onChange(newValue);
			}
			if (update.docChanged || update.selectionSet) {
				const pos = update.state.selection.main.head;
				const line = update.state.doc.lineAt(pos);
				onCursorChange({ line: line.number, col: pos - line.from + 1 });
			}
		});

		const startState = cm.EditorState.create({
			doc,
			extensions: [
				runKeyBinding,
				cm.basicSetup,
				language === 'sql' ? cm.sql({ dialect: cm.sqlite, upperCaseKeywords: true }) : cm.python(),
				cm.indentUnit.of(language === 'sql' ? '  ' : '    '),
				cm.EditorView.theme(themeSpec(palette), { dark }),
				cm.syntaxHighlighting(cm.HighlightStyle.define(highlightSpec(cm.tags, palette))),
				updateListener,
				cm.EditorView.lineWrapping,
				cm.EditorView.domEventHandlers({
					wheel: (event: WheelEvent) => {
						if (!event.ctrlKey && !event.metaKey) return false;
						event.preventDefault();
						zoomEditor(event.deltaY < 0 ? 1 : -1);
						return true;
					}
				})
			]
		});

		editorView = new cm.EditorView({ state: startState, parent: editorContainer });
		reindent = () => {
			if (!editorView || !cm) return;
			const changes = cm.indentRange(editorView.state, 0, editorView.state.doc.length);
			if (!changes.empty) editorView.dispatch({ changes });
		};
	}

	onMount(() => {
		loadCm().then(() => rebuildEditor(value));
	});

	// Picking another theme rebuilds the editor with its colours, keeping the code.
	$effect(() => {
		void palette;
		void dark;
		if (editorView) rebuildEditor(editorView.state.doc.toString());
	});

	$effect(() => {
		// `value` must be read unconditionally, before the `editorView` guard --
		// on the effect's first run (during mount, before loadCm() resolves)
		// editorView is still null, so a read gated behind `if (editorView)`
		// never happens on that pass. Svelte's $effect tracks only what's
		// actually read on a given run, and editorView itself is a plain
		// (non-reactive) variable, so a dependency on `value` that's never
		// established on the first run is never established at all -- the
		// effect goes permanently inert, and later external changes to
		// `value` (Reset, Re-attempt) stop reaching the editor's own display.
		const nextValue = value;
		if (editorView) {
			const currentDoc = editorView.state.doc.toString();
			if (nextValue !== currentDoc) {
				editorView.dispatch({ changes: { from: 0, to: currentDoc.length, insert: nextValue } });
			}
		}
	});

	// The theme reads the size from this CSS variable, so zooming never rebuilds the editor.
	$effect(() => {
		editorContainer?.style.setProperty('--editor-font-size', `${fontSize}px`);
		editorView?.requestMeasure();
	});

	onDestroy(() => editorView?.destroy());
</script>

<div
	class="relative h-full w-full overflow-hidden"
	style:background={palette.bg}
	bind:this={editorContainer}
></div>

<style>
	:global(.cm-editor) {
		height: 100%;
		outline: none !important;
	}
</style>
