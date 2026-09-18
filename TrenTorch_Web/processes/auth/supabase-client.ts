import { createClient, type SupabaseClient } from '@supabase/supabase-js';
import { browser } from '$app/environment';
import { PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY } from '$env/static/public';

// Auth is client-only: the site is a fully prerendered static build with no
// server, so there is nothing to run this against during SSR/prerender --
// only construct the client once something in the browser actually asks
// for it, never at module eval.
let client: SupabaseClient | null = null;

export function getSupabaseClient(): SupabaseClient {
	if (!browser) {
		throw new Error('getSupabaseClient() must only be called in the browser');
	}
	if (!client) {
		client = createClient(PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY);
	}
	return client;
}
