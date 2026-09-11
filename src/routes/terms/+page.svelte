<script lang="ts">
	const LAST_UPDATED = 'September 12, 2026';
</script>

<svelte:head>
	<title>Terms</title>
	<meta name="description" content="Terms of use for TrenTorch-Web." />
</svelte:head>

<div class="container max-w-3xl px-4 py-12 md:px-6">
	<h1 class="mb-1 font-mono text-2xl font-bold tracking-tight">Terms</h1>
	<p class="mb-8 text-sm text-muted-foreground">Last updated: {LAST_UPDATED}</p>

	<div class="question-prose">
		<h2>What this is</h2>
		<p>
			TrenTorch-Web is a free, open source, educational project: an in-browser IDE for a curriculum
			of ML/PyTorch implementation questions. There is no payment, no paid tier, and no account
			required to use it.
		</p>

		<h2>License</h2>
		<p>
			The site, its source code, and the curriculum content are <a
				href="https://github.com/TrenTorch/TrenTorch-Web/blob/main/LICENSE">MIT licensed</a
			>. You're free to read, fork, modify, and reuse any of it, including the questions themselves,
			under the terms of that license.
		</p>

		<h2>Not affiliated with PyTorch or Meta</h2>
		<p>
			TrenTorch-Web is an independent, community-built project. Question content is written to
			mirror the real <code>torch.nn.functional</code> API for learning purposes, but this project is
			not affiliated with, endorsed by, or sponsored by Meta, the PyTorch Foundation, or the PyTorch project.
			"PyTorch" is a trademark of its respective owner, referenced here only for accurate technical description.
		</p>

		<h2>Educational content, provided as-is</h2>
		<p>
			The curriculum, oracle solutions, and test suites are written and reviewed by the project's
			maintainers and contributors, but this is an evolving educational resource, not an official
			reference. It's provided without warranty of any kind: correctness, fitness for a particular
			purpose, or otherwise. If you find a bug in a question, theory explanation, or test, please
			<a href="https://github.com/TrenTorch/TrenTorch-Web/issues">open an issue</a>.
		</p>

		<h2>Acceptable use</h2>
		<p>
			Use the site the way it's meant to be used: solving questions, reading the curriculum,
			contributing to the project. Don't attempt to disrupt the site, abuse its infrastructure, or
			use it in a way that violates the project's
			<a href="https://github.com/TrenTorch/TrenTorch-Web/blob/main/CODE_OF_CONDUCT.md">
				Code of Conduct
			</a>.
		</p>

		<h2>No warranty, limitation of liability</h2>
		<p>
			The site is provided "as is," without warranty of any kind, express or implied, consistent
			with its MIT license. The maintainers aren't liable for any damages arising from your use of
			the site.
		</p>

		<h2>Changes</h2>
		<p>
			These terms may change as the project evolves. Material changes will update the date at the
			top of this page.
		</p>

		<h2>Contact</h2>
		<p>
			Questions about these terms, or anything else: <a
				href="https://github.com/TrenTorch/TrenTorch-Web/issues">open an issue on GitHub</a
			>.
		</p>
	</div>
</div>
