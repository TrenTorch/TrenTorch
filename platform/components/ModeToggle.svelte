<script lang="ts">
	import { Sun, Moon } from '@lucide/svelte';

	function toggle() {
		const dark = document.documentElement.classList.toggle('dark');
		try {
			localStorage.setItem('theme', dark ? 'dark' : 'light');
		} catch {
			// localStorage unavailable: theme just won't persist across visits.
		}
	}
</script>

<button
	type="button"
	onclick={toggle}
	aria-label="Toggle theme"
	class="inline-flex size-9 shrink-0 items-center justify-center rounded-md transition-colors hover:bg-accent hover:text-accent-foreground"
>
	<Sun class="size-[1.2rem] scale-100 rotate-0 transition-all dark:scale-0 dark:-rotate-90" />
	<Moon
		class="absolute size-[1.2rem] scale-0 rotate-90 transition-all dark:scale-100 dark:rotate-0"
	/>
</button>
