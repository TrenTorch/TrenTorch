<script lang="ts">
	import { browser } from '$app/environment';
	import { NotebookPen, Trash, Check } from '@lucide/svelte';

	interface Props {
		/** Identifies the paper; notes are saved separately for each one. */
		storageId: string;
		title: string;
	}

	let { storageId, title }: Props = $props();

	const SAVE_DELAY_MS = 400;
	const MAX_LENGTH = 50_000;

	let text = $state('');
	let savedAt = $state<number | null>(null);
	let status = $state<'idle' | 'saving' | 'saved' | 'unsaved'>('idle');
	let loadedKey: string | null = null;
	let timer: ReturnType<typeof setTimeout> | undefined;

	const storageKey = $derived(`trentorch:paper-notes:v1:${storageId}`);
	const words = $derived(text.trim() === '' ? 0 : text.trim().split(/\s+/).length);

	function read(key: string): { text: string; savedAt: number | null } {
		try {
			const raw = localStorage.getItem(key);
			if (!raw) return { text: '', savedAt: null };
			const data = JSON.parse(raw) as { text?: unknown; savedAt?: unknown };
			return {
				text: typeof data.text === 'string' ? data.text.slice(0, MAX_LENGTH) : '',
				savedAt: typeof data.savedAt === 'number' ? data.savedAt : null
			};
		} catch {
			return { text: '', savedAt: null };
		}
	}

	function write(key: string, value: string) {
		try {
			if (value.trim() === '') {
				localStorage.removeItem(key);
				savedAt = null;
			} else {
				const now = Date.now();
				localStorage.setItem(key, JSON.stringify({ v: 1, text: value, savedAt: now }));
				savedAt = now;
			}
			status = 'saved';
		} catch {
			// storage blocked or full: the notes stay in the box but are not persisted
			status = 'unsaved';
		}
	}

	// Load when the paper changes. Declared before the save effect so a new paper
	// never overwrites its own notes with the previous paper's text.
	$effect(() => {
		const key = storageKey;
		if (!browser) return;
		clearTimeout(timer);
		const stored = read(key);
		text = stored.text;
		savedAt = stored.savedAt;
		status = 'idle';
		loadedKey = key;
	});

	function onInput() {
		const key = storageKey;
		if (loadedKey !== key) return;
		status = 'saving';
		clearTimeout(timer);
		timer = setTimeout(() => write(key, text), SAVE_DELAY_MS);
	}

	// Save immediately when leaving the page so the last keystrokes are not lost.
	function flush() {
		if (status !== 'saving' || loadedKey !== storageKey) return;
		clearTimeout(timer);
		write(storageKey, text);
	}

	function clearNotes() {
		if (text.trim() === '') return;
		if (!window.confirm('Delete all notes for this paper?')) return;
		clearTimeout(timer);
		text = '';
		write(storageKey, '');
	}

	function formatTime(ms: number): string {
		return new Date(ms).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' });
	}

	$effect(() => () => clearTimeout(timer));
</script>

<svelte:window onbeforeunload={flush} onpagehide={flush} />

<aside
	class="flex min-h-[18rem] flex-col overflow-hidden rounded-2xl border border-white/10 bg-[#0b0b0d] shadow-2xl shadow-black/40"
	aria-label="Notes for {title}"
>
	<div
		class="flex items-center justify-between gap-3 border-b border-white/10 bg-[#141417] px-4 py-2.5 text-xs text-white/70"
	>
		<h2 class="flex items-center gap-2 text-sm font-medium text-white">
			<NotebookPen class="size-4 text-white/60" />
			Notes
		</h2>
		<p class="flex items-center gap-1.5 font-mono tracking-wide" aria-live="polite">
			{#if status === 'saving'}
				<span class="text-white/50">Saving…</span>
			{:else if status === 'unsaved'}
				<span class="text-amber-400">Could not save</span>
			{:else if savedAt}
				<Check class="size-3.5 text-emerald-400" />
				<span class="text-white/50">Saved {formatTime(savedAt)}</span>
			{:else}
				<span class="text-white/40">Saved in this browser</span>
			{/if}
		</p>
	</div>

	<textarea
		bind:value={text}
		oninput={onInput}
		maxlength={MAX_LENGTH}
		spellcheck="true"
		placeholder="Thoughts, questions, things to come back to…

Anything you type here is saved automatically in this browser."
		aria-label="Your notes on this paper"
		class="min-h-0 flex-1 resize-none bg-transparent px-4 py-4 text-sm leading-relaxed text-white/90 placeholder:text-white/30 focus:outline-none"
	></textarea>

	<div
		class="flex items-center justify-between gap-3 border-t border-white/10 bg-[#101013] px-4 py-2 text-xs text-white/50"
	>
		<span class="font-mono tabular-nums">{words} {words === 1 ? 'word' : 'words'}</span>
		<button
			type="button"
			onclick={clearNotes}
			disabled={text.trim() === ''}
			class="inline-flex items-center gap-1.5 rounded-md px-2 py-1 transition-colors hover:bg-white/10 hover:text-white focus-visible:ring-2 focus-visible:ring-white/40 focus-visible:outline-none disabled:opacity-30"
		>
			<Trash class="size-3.5" /> Clear
		</button>
	</div>
</aside>
