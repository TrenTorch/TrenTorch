<script lang="ts">
	import { resolve } from '$app/paths';
</script>

<footer class="border-t py-6 md:px-8">
	<div class="container flex flex-col items-center justify-between gap-2 md:flex-row">
		<p class="text-center text-sm leading-loose text-balance text-muted-foreground md:text-left">
			TrenTorch-Web is open source, the web front for the TrenTorch curriculum,
			<a
				href="https://github.com/TrenTorch/TrenTorch-Web/blob/main/LICENSE"
				class="font-medium underline underline-offset-4 hover:text-foreground"
			>
				MIT licensed
			</a>
			, and follows a
			<a
				href="https://github.com/TrenTorch/TrenTorch-Web/blob/main/CODE_OF_CONDUCT.md"
				class="font-medium underline underline-offset-4 hover:text-foreground"
			>
				Code of Conduct
			</a>
			.
		</p>
		<p class="font-mono text-sm text-muted-foreground">
			<a href="https://github.com/TrenTorch" class="transition-colors hover:text-foreground">
				github.com/TrenTorch
			</a>
		</p>
	</div>
	<div
		class="container mt-3 flex flex-col items-center justify-between gap-2 border-t border-border pt-3 text-xs text-muted-foreground md:flex-row"
	>
		<p>&copy; {new Date().getFullYear()} TrenTorch</p>
		<nav class="flex items-center gap-4">
			<a href={resolve('/terms')} class="transition-colors hover:text-foreground"> Terms </a>
			<a href={resolve('/privacy')} class="transition-colors hover:text-foreground"> Privacy </a>
		</nav>
	</div>
</footer>
