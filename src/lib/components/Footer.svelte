<script lang="ts">
	import { resolve } from '$app/paths';
</script>

<footer class="border-t py-6 md:px-8">
	<div class="container flex flex-col items-center justify-between gap-3 md:flex-row">
		<p class="text-center text-sm leading-loose text-balance text-muted-foreground md:text-left">
			&copy; {new Date().getFullYear()} TrenTorch. Source-available, free for
			<a
				href="https://github.com/TrenTorch/TrenTorch-Web/blob/main/LICENSE"
				class="font-medium underline underline-offset-4 hover:text-foreground"
			>
				personal and educational use
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
		<nav class="flex items-center gap-4 font-mono text-sm text-muted-foreground">
			<a href="https://github.com/TrenTorch" class="transition-colors hover:text-foreground">
				github.com/TrenTorch
			</a>
			<a href={resolve('/terms')} class="transition-colors hover:text-foreground">Terms</a>
			<a href={resolve('/privacy')} class="transition-colors hover:text-foreground">Privacy</a>
		</nav>
	</div>
</footer>
