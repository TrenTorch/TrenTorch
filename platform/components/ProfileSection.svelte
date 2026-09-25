<script lang="ts">
	import { Input } from '$components/ui/input';
	import { Textarea } from '$components/ui/textarea';
	import { Checkbox } from '$components/ui/checkbox';
	import Button from '$components/Button.svelte';
	import { session } from '$processes/auth/session.svelte';
	import { signInPrompt } from '$processes/auth/sign-in-prompt.svelte';
	import { loadProfile, saveProfile } from '$processes/profile/profile-store';
	import { prefillFromAccount } from '$processes/profile/prefill-from-account';
	import { profileState } from '$processes/profile/profile-state.svelte';
	import {
		validateProfile,
		LIMITS,
		type ProfileForm,
		type ProfileErrors
	} from '$processes/profile/validate-profile';

	const blank: ProfileForm = {
		displayName: '',
		username: '',
		organization: '',
		jobTitle: '',
		altEmail: '',
		bio: '',
		location: '',
		xUrl: '',
		linkedinUrl: '',
		scholarUrl: '',
		githubUrl: '',
		websiteUrl: '',
		isPublic: false
	};

	let form = $state<ProfileForm>({ ...blank });
	let errors = $state<ProfileErrors>({});
	let prefilled = $state(false);
	// Saved details open read-only so a stray keystroke cannot change them.
	let editing = $state(true);
	let saved = $state<ProfileForm | null>(null);
	let copied = $state(false);
	const origin = typeof window === 'undefined' ? '' : window.location.origin;
	const sharePath = $derived(`/accounts/@${saved?.username ?? ''}`);
	const shareUrl = $derived(`${origin}${sharePath}`);
	const shareLabel = $derived(`${origin.replace(/^https?:\/\//, '')}${sharePath}`);

	async function copyLink() {
		try {
			await navigator.clipboard.writeText(shareUrl);
			copied = true;
			setTimeout(() => (copied = false), 2000);
		} catch {
			// Clipboard blocked: the link above is still selectable.
		}
	}
	const hasData = (value: ProfileForm) => Object.values(value).some((v) => v !== '' && v !== false);
	let status = $state<'loading' | 'ready' | 'unavailable' | 'saving'>('loading');
	let message = $state<{ kind: 'ok' | 'error'; text: string } | null>(null);

	const locked = $derived(status === 'loading' || !editing);

	const userId = $derived(session.user?.id ?? null);

	$effect(() => {
		const id = userId;
		if (!id) return;
		status = 'loading';
		loadProfile(id).then((loaded) => {
			if (userId !== id) return;
			if (loaded) {
				profileState.set({ ...loaded });
				const suggested = session.user ? prefillFromAccount(loaded, session.user) : null;
				form = suggested?.form ?? loaded;
				prefilled = suggested?.filled ?? false;
				saved = hasData(loaded) ? { ...loaded } : null;
				editing = saved === null || prefilled;
				status = 'ready';
			} else {
				status = 'unavailable';
			}
		});
	});

	function startEditing() {
		message = null;
		editing = true;
	}

	function cancelEditing() {
		if (saved) form = { ...saved };
		errors = {};
		message = null;
		prefilled = false;
		editing = false;
	}

	async function onSubmit(event: SubmitEvent) {
		event.preventDefault();
		if (!userId || status === 'saving' || !editing) return;
		message = null;
		const { errors: found, clean } = validateProfile(form);
		errors = found;
		if (Object.keys(found).length > 0) return;
		status = 'saving';
		const result = await saveProfile(userId, clean);
		status = 'ready';
		if (result.ok) {
			form = clean;
			prefilled = false;
			saved = { ...clean };
			editing = false;
			profileState.set({ ...clean });
			message = { kind: 'ok', text: 'Profile saved.' };
		} else {
			if (result.field) errors = { [result.field]: result.message };
			message = { kind: 'error', text: result.message };
		}
	}

	type TextField = Exclude<keyof ProfileForm, 'isPublic'>;

	const fields: { key: TextField; label: string; placeholder: string; wide?: boolean }[] = [
		{ key: 'displayName', label: 'Full name', placeholder: 'Ada Lovelace' },
		{ key: 'username', label: 'Username', placeholder: 'ada_l' },
		{ key: 'organization', label: 'College or company', placeholder: 'IIT Bombay' },
		{ key: 'jobTitle', label: 'Role', placeholder: 'Student, ML engineer, researcher' },
		{ key: 'altEmail', label: 'Alternate email', placeholder: 'you@example.com' },
		{ key: 'location', label: 'Location', placeholder: 'Mumbai, India' },
		{ key: 'xUrl', label: 'X', placeholder: '@handle or profile link' },
		{ key: 'linkedinUrl', label: 'LinkedIn', placeholder: 'Profile link or handle' },
		{
			key: 'scholarUrl',
			label: 'Google Scholar',
			placeholder: 'scholar.google.com/citations?user=...'
		},
		{ key: 'githubUrl', label: 'GitHub', placeholder: '@handle or profile link' },
		{ key: 'websiteUrl', label: 'Website', placeholder: 'https://your-site.com', wide: true }
	];
</script>

<div class="rounded-2xl border border-foreground p-6">
	<h2 class="mb-1 font-mono font-semibold">Profile</h2>
	<p class="mb-5 text-sm text-muted-foreground">
		Tell us a bit about you. Everything here is optional and only visible to you unless you make
		your profile public.
	</p>

	{#if !userId}
		<p class="text-sm text-muted-foreground">
			<button
				type="button"
				class="underline hover:text-foreground"
				onclick={() => signInPrompt.open()}>Sign in</button
			> to set up your profile.
		</p>
	{:else if status === 'unavailable'}
		<p class="text-sm text-muted-foreground">
			Profile details are not available right now. Please try again later.
		</p>
	{:else}
		{#if prefilled}
			<p class="mb-4 text-xs text-muted-foreground" role="status">
				We filled in a few details from your account. Review them and press Save to keep them.
			</p>
		{/if}
		<form class="space-y-5" onsubmit={onSubmit} aria-busy={status === 'loading'}>
			<div class="grid gap-4 sm:grid-cols-2">
				{#each fields as field (field.key)}
					<label class="block space-y-1.5 {field.wide ? 'sm:col-span-2' : ''}">
						<span class="text-xs font-medium text-muted-foreground">{field.label}</span>
						<Input
							bind:value={form[field.key]}
							placeholder={field.placeholder}
							disabled={locked}
							autocomplete="off"
							aria-invalid={errors[field.key] ? true : undefined}
							class="rounded-lg"
						/>
						{#if errors[field.key]}
							<span class="block text-xs text-destructive">{errors[field.key]}</span>
						{/if}
					</label>
				{/each}
				<label class="block space-y-1.5 sm:col-span-2">
					<span class="flex justify-between text-xs font-medium text-muted-foreground">
						Short bio
						<span class="tabular-nums">{form.bio.length}/{LIMITS.bio}</span>
					</span>
					<Textarea
						bind:value={form.bio}
						rows={3}
						maxlength={LIMITS.bio}
						disabled={locked}
						placeholder="What are you learning or building?"
						class="rounded-lg"
					/>
					{#if errors.bio}
						<span class="block text-xs text-destructive">{errors.bio}</span>
					{/if}
				</label>
			</div>

			<label class="flex items-start gap-2 text-sm">
				<Checkbox bind:checked={form.isPublic} disabled={locked} class="mt-0.5" />
				<span>
					Make my profile public
					<span class="block text-xs text-muted-foreground">
						Off by default. Anyone with your link can see your name, bio, links, rating and solved
						count. Your email is never shown. You need a username.
					</span>
				</span>
			</label>

			{#if saved?.isPublic && saved.username && !editing}
				<div class="flex flex-wrap items-center gap-2 text-sm">
					<!-- eslint-disable svelte/no-navigation-without-resolve -->
					<a class="underline underline-offset-2" href={shareUrl} target="_blank" rel="noopener">
						{shareLabel}
					</a>
					<!-- eslint-enable svelte/no-navigation-without-resolve -->
					<Button type="button" variant="outline" size="sm" class="rounded-xl!" onclick={copyLink}>
						{copied ? 'Copied' : 'Copy link'}
					</Button>
				</div>
			{/if}

			<div class="flex items-center gap-3">
				{#if editing}
					<Button type="submit" size="sm" class="rounded-xl!" disabled={status !== 'ready'}>
						{status === 'saving' ? 'Saving...' : 'Save profile'}
					</Button>
					{#if saved}
						<Button
							type="button"
							variant="outline"
							size="sm"
							class="rounded-xl!"
							onclick={cancelEditing}
							disabled={status === 'saving'}
						>
							Cancel
						</Button>
					{/if}
				{:else}
					<Button
						type="button"
						variant="outline"
						size="sm"
						class="rounded-xl!"
						onclick={startEditing}
						disabled={status !== 'ready'}
					>
						Edit profile
					</Button>
				{/if}
				{#if message}
					<span
						class="text-sm {message.kind === 'ok' ? 'text-foreground' : 'text-destructive'}"
						role="status">{message.text}</span
					>
				{/if}
			</div>
		</form>
	{/if}
</div>
