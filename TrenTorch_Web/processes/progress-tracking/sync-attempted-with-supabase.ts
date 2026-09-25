import { attempted } from './attempted.svelte';
import { fetchAttempted, upsertAttempted } from './supabase-drafts-store';

// Same two-way union as sync-solved-with-supabase.ts: attempts made on
// another device are pulled in, local ones Supabase lacks are pushed up.
export async function syncAttemptedWithSupabase(userId: string): Promise<void> {
	const remote = await fetchAttempted(userId);
	if (remote === null) return;
	const remoteSet = new Set(remote);
	for (const slug of remoteSet) attempted.markAttemptedFromRemote(slug);
	await upsertAttempted(
		userId,
		[...attempted.slugs].filter((slug) => !remoteSet.has(slug))
	);
}
