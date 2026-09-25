import { getSupabaseClient } from '$processes/auth/supabase-client';

export type DeleteResult = { ok: true } | { ok: false; message: string };

// Everything this site keeps in the browser is namespaced trentorch-* or
// trentorch_*: code drafts, solved and attempted lists, layout choices.
function clearLocalData() {
	try {
		for (const key of Object.keys(localStorage)) {
			if (key.startsWith('trentorch')) localStorage.removeItem(key);
		}
	} catch {
		// Storage blocked: nothing local to clear.
	}
}

export async function deleteAccount(): Promise<DeleteResult> {
	try {
		const supabase = getSupabaseClient();
		const { error } = await supabase
			.rpc('delete_my_account')
			.abortSignal(AbortSignal.timeout(15_000));
		if (error) {
			console.error('Failed to delete account', error);
			return { ok: false, message: 'Could not delete your account. Try again in a moment.' };
		}
		await supabase.auth.signOut().catch(() => undefined);
		clearLocalData();
		return { ok: true };
	} catch {
		return {
			ok: false,
			message: 'Could not delete your account. Check your connection and try again.'
		};
	}
}
