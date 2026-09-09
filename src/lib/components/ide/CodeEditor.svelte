<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { EditorView, basicSetup } from 'codemirror';
	import { EditorState } from '@codemirror/state';
	import { python } from '@codemirror/lang-python';
	import { keymap } from '@codemirror/view';

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
	let editorView: EditorView | null = null;

	// Dark theme — used when <html> has class="dark"
	const darkTheme = EditorView.theme(
		{
			'&': {
				height: '100%',
				backgroundColor: '#000000',
				color: '#ededed',
				fontFamily: "'Geist Mono', 'JetBrains Mono', ui-monospace, Menlo, monospace",
				fontSize: '13px'
			},
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
		},
		{ dark: true }
	);

	// Light theme — used when <html> does NOT have class="dark"
	const lightTheme = EditorView.theme(
		{
			'&': {
				height: '100%',
				backgroundColor: '#ffffff',
				color: '#171717',
				fontFamily: "'Geist Mono', 'JetBrains Mono', ui-monospace, Menlo, monospace",
				fontSize: '13px'
			},
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
		},
		{ dark: false }
	);

	function isDarkMode(): boolean {
		return document.documentElement.classList.contains('dark');
	}

	function rebuildEditor(doc: string) {
		editorView?.destroy();

		const runKeyBinding = keymap.of([
			{
				key: 'Mod-Enter',
				run: () => {
					onRun();
					return true;
				}
			},
			{
				key: 'Shift-Enter',
				run: () => {
					onRun();
					return true;
				}
			}
		]);

		const updateListener = EditorView.updateListener.of((update) => {
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

		const startState = EditorState.create({
			doc,
			extensions: [
				basicSetup,
				python(),
				isDarkMode() ? darkTheme : lightTheme,
				runKeyBinding,
				updateListener,
				EditorView.lineWrapping
			]
		});

		editorView = new EditorView({ state: startState, parent: editorContainer });
	}

	onMount(() => {
		rebuildEditor(value);

		// Watch for class changes on <html> to switch themes reactively
		const observer = new MutationObserver(() => {
			const currentDoc = editorView?.state.doc.toString() ?? value;
			rebuildEditor(currentDoc);
		});
		observer.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });

		return () => observer.disconnect();
	});

	$effect(() => {
		if (editorView) {
			const currentDoc = editorView.state.doc.toString();
			if (value !== currentDoc) {
				editorView.dispatch({
					changes: { from: 0, to: currentDoc.length, insert: value }
				});
			}
		}
	});

	onDestroy(() => {
		editorView?.destroy();
	});
</script>

<div class="relative h-full w-full overflow-hidden bg-background" bind:this={editorContainer}></div>

<style>
	:global(.cm-editor) {
		height: 100%;
		outline: none !important;
	}
</style>
