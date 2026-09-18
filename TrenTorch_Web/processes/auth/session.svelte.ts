import { browser } from '$app/environment';
import type { Session, User } from '@supabase/supabase-js';
import { getSupabaseClient } from './supabase-client';

// One module-level $state pair, subscribed to Supabase's own
// onAuthStateChange once in the browser -- every component reads through
// the `session` export below rather than each keeping its own
// getSession() call, so a sign-in/sign-out anywhere in the app is
// reflected everywhere else immediately.
let currentSession = $state<Session | null>(null);
let isLoading = $state(true);

if (browser) {
	const supabase = getSupabaseClient();
	supabase.auth.getSession().then(({ data }) => {
		currentSession = data.session;
		isLoading = false;
	});
	supabase.auth.onAuthStateChange((_event, newSession) => {
		currentSession = newSession;
		isLoading = false;
	});
}

export const session = {
	get current(): Session | null {
		return currentSession;
	},
	get user(): User | null {
		return currentSession?.user ?? null;
	},
	get isLoading(): boolean {
		return isLoading;
	}
};

function redirectTo(): string {
	return `${window.location.origin}/account`;
}

export async function signInWithGitHub() {
	const supabase = getSupabaseClient();
	await supabase.auth.signInWithOAuth({
		provider: 'github',
		options: { redirectTo: redirectTo() }
	});
}

export async function signInWithGoogle() {
	const supabase = getSupabaseClient();
	await supabase.auth.signInWithOAuth({
		provider: 'google',
		options: { redirectTo: redirectTo() }
	});
}

export async function signInWithMagicLink(email: string) {
	const supabase = getSupabaseClient();
	const { error } = await supabase.auth.signInWithOtp({
		email,
		options: { emailRedirectTo: redirectTo() }
	});
	if (error) throw error;
}

export async function signOut() {
	const supabase = getSupabaseClient();
	await supabase.auth.signOut();
}
