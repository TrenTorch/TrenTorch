<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import type { EditorView as EditorViewType } from '@codemirror/view';

	// CodeMirror (~1 MB of source across @codemirror/*) loads via a dynamic
	// import inside onMount, never a static import: it is a client-only
	// editor, and a static import drags the whole thing into the SSR /
	// serverless bundle where it is dead weight that also slows cold starts.
	/* eslint-disable @typescript-eslint/no-explicit-any */

	let {
		value = $bindable(''),
		onRun = () => {},
		onChange = () => {},
		onCursorChange = () => {}
	} = $props<{
		value: string;
		onRun?: (val?: void) => void;
		onChange?: (val: string) => void;
		onCursorChange?: (pos: { line: number; col: number }) => void;
	}>();

	let editorContainer: HTMLDivElement;
	let editorView: EditorViewType | null = null;

	// Populated once CodeMirror has loaded. Everything that touches these
	// runs after loadCm() resolves, so nothing here executes at module eval.
	let cm: {
		EditorView: any;
		EditorState: any;
		basicSetup: any;
		python: any;
		keymap: any;
		HighlightStyle: any;
		syntaxHighlighting: any;
		tags: any;
	} | null = null;
	let darkTheme: any;
	let lightTheme: any;
	let darkHighlight: any;
	let lightHighlight: any;

	// Plain style specs (no CodeMirror needed to define them); turned into
	// real EditorView.theme extensions in loadCm once EditorView exists.
	// Colors match GitHub's own Dark/Light editor themes exactly (editor
	// chrome from github-vscode-theme's `editor.*` tokens), so the in-browser
	// IDE reads the same as viewing this code on github.com.
	const sharedRoot = {
		height: '100%',
		fontFamily: "'Geist Mono', 'JetBrains Mono', ui-monospace, Menlo, monospace",
		fontSize: '13px'
	};
	const darkThemeSpec = {
		'&': { ...sharedRoot, backgroundColor: '#0d1117', color: '#c9d1d9' },
		'.cm-content': { padding: '12px 0', caretColor: '#c9d1d9' },
		'.cm-cursor, .cm-dropCursor': { borderLeftColor: '#c9d1d9', borderLeftWidth: '2px' },
		'&.cm-focused .cm-selectionBackground, .cm-selectionBackground, .cm-content ::selection': {
			backgroundColor: '#3392ff44 !important'
		},
		'.cm-gutters': {
			backgroundColor: '#0d1117',
			color: '#6e7681',
			borderRight: '1px solid #21262d',
			paddingRight: '6px'
		},
		'.cm-activeLineGutter': { backgroundColor: '#6e768114', color: '#c9d1d9' },
		'.cm-activeLine': { backgroundColor: '#6e768114' },
		'.cm-line': { padding: '0 12px' },
		'.cm-scroller': { overflow: 'auto', lineHeight: '1.6' },
		'.cm-matchingBracket, .cm-nonmatchingBracket': {
			backgroundColor: '#3392ff44',
			outline: 'none'
		}
	};
	const lightThemeSpec = {
		'&': { ...sharedRoot, backgroundColor: '#ffffff', color: '#1f2328' },
		'.cm-content': { padding: '12px 0', caretColor: '#1f2328' },
		'.cm-cursor, .cm-dropCursor': { borderLeftColor: '#1f2328', borderLeftWidth: '2px' },
		'&.cm-focused .cm-selectionBackground, .cm-selectionBackground, .cm-content ::selection': {
			backgroundColor: '#0969da33 !important'
		},
		'.cm-gutters': {
			backgroundColor: '#ffffff',
			color: '#8c959f',
			borderRight: '1px solid #d1d9e0',
			paddingRight: '6px'
		},
		'.cm-activeLineGutter': { backgroundColor: '#eaeef2', color: '#1f2328' },
		'.cm-activeLine': { backgroundColor: '#eaeef280' },
		'.cm-line': { padding: '0 12px' },
		'.cm-scroller': { overflow: 'auto', lineHeight: '1.6' },
		'.cm-matchingBracket, .cm-nonmatchingBracket': {
			backgroundColor: '#0969da33',
			outline: 'none'
		}
	};

	// Syntax token colors, also lifted straight from GitHub's own
	// github-vscode-theme (the Dark and Light variants) rather than
	// CodeMirror's generic defaults.
	function buildHighlightSpecs(t: any) {
		return {
			dark: [
				{ tag: t.comment, color: '#8b949e', fontStyle: 'italic' },
				{
					tag: [t.keyword, t.controlKeyword, t.moduleKeyword, t.operatorKeyword],
					color: '#ff7b72'
				},
				{ tag: [t.definitionKeyword, t.self], color: '#ff7b72' },
				{
					tag: [t.function(t.variableName), t.function(t.definition(t.variableName))],
					color: '#d2a8ff'
				},
				{ tag: t.className, color: '#f2cc60' },
				{ tag: t.definition(t.className), color: '#f2cc60' },
				{ tag: [t.string, t.special(t.string), t.docString], color: '#a5d6ff' },
				{ tag: [t.number, t.bool, t.null], color: '#79c0ff' },
				{ tag: t.operator, color: '#ff7b72' },
				{ tag: t.punctuation, color: '#c9d1d9' },
				{ tag: t.propertyName, color: '#79c0ff' },
				{ tag: [t.variableName, t.definition(t.variableName)], color: '#ffa657' },
				{ tag: t.typeName, color: '#f2cc60' },
				{ tag: t.meta, color: '#d2a8ff' },
				{ tag: t.invalid, color: '#f85149' }
			],
			light: [
				{ tag: t.comment, color: '#6e7781', fontStyle: 'italic' },
				{
					tag: [t.keyword, t.controlKeyword, t.moduleKeyword, t.operatorKeyword],
					color: '#cf222e'
				},
				{ tag: [t.definitionKeyword, t.self], color: '#cf222e' },
				{
					tag: [t.function(t.variableName), t.function(t.definition(t.variableName))],
					color: '#8250df'
				},
				{ tag: t.className, color: '#953800' },
				{ tag: t.definition(t.className), color: '#953800' },
				{ tag: [t.string, t.special(t.string), t.docString], color: '#0a3069' },
				{ tag: [t.number, t.bool, t.null], color: '#0550ae' },
				{ tag: t.operator, color: '#cf222e' },
				{ tag: t.punctuation, color: '#1f2328' },
				{ tag: t.propertyName, color: '#0550ae' },
				{ tag: [t.variableName, t.definition(t.variableName)], color: '#953800' },
				{ tag: t.typeName, color: '#953800' },
				{ tag: t.meta, color: '#8250df' },
				{ tag: t.invalid, color: '#82071e' }
			]
		};
	}

	function isDarkMode(): boolean {
		return document.documentElement.classList.contains('dark');
	}

	async function loadCm() {
		const [cmMod, stateMod, pyMod, viewMod, langMod, highlightMod] = await Promise.all([
			import('codemirror'),
			import('@codemirror/state'),
			import('@codemirror/lang-python'),
			import('@codemirror/view'),
			import('@codemirror/language'),
			import('@lezer/highlight')
		]);
		cm = {
			EditorView: cmMod.EditorView,
			basicSetup: cmMod.basicSetup,
			EditorState: stateMod.EditorState,
			python: pyMod.python,
			keymap: viewMod.keymap,
			HighlightStyle: langMod.HighlightStyle,
			syntaxHighlighting: langMod.syntaxHighlighting,
			tags: highlightMod.tags
		};
		darkTheme = cm.EditorView.theme(darkThemeSpec, { dark: true });
		lightTheme = cm.EditorView.theme(lightThemeSpec, { dark: false });
		const specs = buildHighlightSpecs(cm.tags);
		darkHighlight = cm.syntaxHighlighting(cm.HighlightStyle.define(specs.dark));
		lightHighlight = cm.syntaxHighlighting(cm.HighlightStyle.define(specs.light));
	}

	function rebuildEditor(doc: string) {
		if (!cm) return;
		editorView?.destroy();

		const runKeyBinding = cm.keymap.of([
			{ key: 'Mod-Enter', run: () => (onRun(), true) },
			{ key: 'Shift-Enter', run: () => (onRun(), true) }
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
				cm.basicSetup,
				cm.python(),
				isDarkMode() ? darkTheme : lightTheme,
				isDarkMode() ? darkHighlight : lightHighlight,
				runKeyBinding,
				updateListener,
				cm.EditorView.lineWrapping
			]
		});

		editorView = new cm.EditorView({ state: startState, parent: editorContainer });
	}

	onMount(() => {
		let observer: MutationObserver | undefined;
		loadCm().then(() => {
			rebuildEditor(value);
			// Rebuild on <html> class change so the editor theme follows the
			// site theme toggle.
			observer = new MutationObserver(() => {
				rebuildEditor(editorView?.state.doc.toString() ?? value);
			});
			observer.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
		});
		return () => observer?.disconnect();
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

	onDestroy(() => editorView?.destroy());
</script>

<div class="relative h-full w-full overflow-hidden bg-background" bind:this={editorContainer}></div>

<style>
	:global(.cm-editor) {
		height: 100%;
		outline: none !important;
	}
</style>
