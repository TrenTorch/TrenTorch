<script lang="ts">
	const LAST_UPDATED = 'September 12, 2026';
</script>

<svelte:head>
	<title>Privacy</title>
	<meta name="description" content="Privacy policy for TrenTorch-Web." />
</svelte:head>

<div class="container max-w-3xl px-4 py-12 md:px-6">
	<h1 class="mb-1 font-mono text-2xl font-bold tracking-tight">Privacy</h1>
	<p class="mb-8 text-sm text-muted-foreground">Last updated: {LAST_UPDATED}</p>

	<div class="question-prose">
		<h2>Short version</h2>
		<p>
			There are no accounts, no sign-in, and nothing you type is sent to a server. Everything this
			site remembers about you lives in your own browser's local storage and never leaves it.
		</p>

		<h2>What we don't collect</h2>
		<p>
			No accounts. No email address. No payment information. No third-party advertising or tracking
			scripts, and no analytics service watching what you click.
		</p>

		<h2>What's stored in your browser</h2>
		<p>
			The IDE and Questions page remember your progress using <code>localStorage</code>, entirely
			client-side:
		</p>
		<ul>
			<li>Which questions you've solved and attempted</li>
			<li>The code you've written for each question, so it's there when you come back</li>
			<li>The IDE's pane layout, and your light/dark theme choice</li>
			<li>Which sections you've collapsed on the Questions page</li>
		</ul>
		<p>
			None of this is sent anywhere. It's tied to your specific browser on your specific device:
			clearing your browser's site data for this domain, or using a different browser or device,
			resets it. It's also why progress doesn't yet sync across devices, there's no server-side
			account to sync it through.
		</p>

		<h2>Third parties your browser talks to</h2>
		<p>
			To run Python in your browser, the IDE loads <a href="https://www.jsdelivr.com/">Pyodide</a> from
			jsDelivr's public CDN. That request goes to jsDelivr, not to us, and is subject to jsDelivr's own
			privacy practices. Like any website, the hosting provider serving these pages processes standard
			web server logs (IP address, user agent, request timestamps) as a normal part of serving the site;
			we don't use that data for tracking or advertising.
		</p>

		<h2>Cookies</h2>
		<p>
			This site doesn't set tracking or advertising cookies. Anything that looks like a "preference"
			(theme, layout) is <code>localStorage</code>, not a cookie.
		</p>

		<h2>Changes</h2>
		<p>
			If real accounts and server-side progress sync are ever added, this policy will be updated to
			describe exactly what changes and why, before that happens.
		</p>

		<h2>Contact</h2>
		<p>
			Questions about this policy: <a href="https://github.com/TrenTorch/TrenTorch-Web/issues"
				>open an issue on GitHub</a
			>.
		</p>
	</div>
</div>
