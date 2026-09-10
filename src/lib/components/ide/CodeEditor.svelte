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
	} | null = null;
	let darkTheme: any;
	let lightTheme: any;

	// Plain style specs (no CodeMirror needed to define them); turned into
	// real EditorView.theme extensions in loadCm once EditorView exists.
	const sharedRoot = {
		height: '100%',
		fontFamily: "'Geist Mono', 'JetBrains Mono', ui-monospace, Menlo, monospace",
		fontSize: '13px'
	};
	const darkThemeSpec = {
		'&': { ...sharedRoot, backgroundColor: '#000000', color: '#ededed' },
		'.cm-content': { padding: '12px 0', caretColor: '#ffffff' },
		'.cm-cursor, .cm-dropCursor': { borderLeftColor: '#ffffff', borderLeftWidth: '2px' },
		'&.cm-focused .cm-selectionBackground, .cm-selectionBackground, .cm-content ::selection': {
			backgroundColor: '#262626 !important'
		},
		'.cm-gutters': {
			backgroundColor: '#000000',
			color: '#525252',
			borderRight: '1px solid #1a1a1a',
			paddingRight: '6px'
		},
		'.cm-activeLineGutter': { backgroundColor: '#0a0a0a', color: '#ededed' },
		'.cm-activeLine': { backgroundColor: '#0d0d0d' },
		'.cm-line': { padding: '0 12px' },
		'.cm-scroller': { overflow: 'auto', lineHeight: '1.6' }
	};
	const lightThemeSpec = {
		'&': { ...sharedRoot, backgroundColor: '#ffffff', color: '#171717' },
		'.cm-content': { padding: '12px 0', caretColor: '#000000' },
		'.cm-cursor, .cm-dropCursor': { borderLeftColor: '#000000', borderLeftWidth: '2px' },
		'&.cm-focused .cm-selectionBackground, .cm-selectionBackground, .cm-content ::selection': {
			backgroundColor: '#e5e5e5 !important'
		},
		'.cm-gutters': {
			backgroundColor: '#fafafa',
			color: '#a3a3a3',
			borderRight: '1px solid #eaeaea',
			paddingRight: '6px'
		},
		'.cm-activeLineGutter': { backgroundColor: '#f5f5f5', color: '#171717' },
		'.cm-activeLine': { backgroundColor: '#f9f9f9' },
		'.cm-line': { padding: '0 12px' },
		'.cm-scroller': { overflow: 'auto', lineHeight: '1.6' }
	};

	function isDarkMode(): boolean {
		return document.documentElement.classList.contains('dark');
	}

	async function loadCm() {
		const [cmMod, stateMod, pyMod, viewMod] = await Promise.all([
			import('codemirror'),
			import('@codemirror/state'),
			import('@codemirror/lang-python'),
			import('@codemirror/view')
		]);
		cm = {
			EditorView: cmMod.EditorView,
			basicSetup: cmMod.basicSetup,
			EditorState: stateMod.EditorState,
			python: pyMod.python,
			keymap: viewMod.keymap
		};
		darkTheme = cm.EditorView.theme(darkThemeSpec, { dark: true });
		lightTheme = cm.EditorView.theme(lightThemeSpec, { dark: false });
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
		if (editorView) {
			const currentDoc = editorView.state.doc.toString();
			if (value !== currentDoc) {
				editorView.dispatch({ changes: { from: 0, to: currentDoc.length, insert: value } });
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
