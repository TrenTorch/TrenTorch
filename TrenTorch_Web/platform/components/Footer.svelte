<script lang="ts">
	import { resolve } from '$app/paths';
</script>

<footer class="border-t border-border py-6 md:px-8">
	<div
		class="container flex flex-col items-center justify-between gap-6 md:flex-row md:items-start"
	>
		<div class="flex flex-col gap-4">
			<p class="text-center text-sm leading-loose text-balance text-muted-foreground md:text-left">
				&copy; {new Date().getFullYear()} TrenTorch. Source-available, free for
				<a
					href="https://github.com/TrenTorch/TrenTorch/blob/TrenTorch-Dev/LICENSE"
					class="font-medium underline underline-offset-4 hover:text-foreground"
				>
					personal and educational use
				</a>
				, and follows a
				<a
					href="https://github.com/TrenTorch/TrenTorch/blob/TrenTorch-Dev/CODE_OF_CONDUCT.md"
					class="font-medium underline underline-offset-4 hover:text-foreground"
				>
					Code of Conduct
				</a>
				.
			</p>

			<!-- Disclaimer for the "Learners signing up from" strip on the landing page -->
			<p
				class="text-center text-xs leading-relaxed text-balance text-muted-foreground md:text-left"
			>
				"Learners signing up from" is based on the email domains people used to sign up, counted in
				aggregate; no individual is named. It does not mean these organizations endorse, sponsor, or
				are affiliated with TrenTorch. All names and trademarks belong to their respective owners.
			</p>
		</div>
		<nav
			class="grid grid-cols-2 gap-x-10 gap-y-1 font-mono text-sm leading-7 text-muted-foreground"
		>
			<a
				href="https://github.com/TrenTorch/TrenTorch"
				class="transition-colors hover:text-foreground"
			>
				GitHub
			</a>
			<a href={resolve('/terms')} class="transition-colors hover:text-foreground">Terms</a>
			<a href={resolve('/privacy')} class="transition-colors hover:text-foreground">Privacy</a>
			<a href={resolve('/contact')} class="transition-colors hover:text-foreground">Contact</a>
			<a
				href="https://discord.gg/2hSsftQCZ9"
				target="_blank"
				rel="noopener noreferrer"
				class="transition-colors hover:text-foreground"
			>
				Discord
			</a>
		</nav>
	</div>
</footer>
