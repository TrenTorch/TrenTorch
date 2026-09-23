// Preview deployments cannot sign in: Supabase only redirects back to the
// production domain, so every sign-in on a preview URL lands on trentorch.com.
// The Cloudflare Pages preview environment sets VITE_PREVIEW_SKIP_SIGN_IN=1 so
// a preview can be tested end to end. Production never sets it, and nothing is
// written to Supabase without a signed-in user, so this cannot touch real data.
export function signInSkipped(): boolean {
	return import.meta.env.VITE_PREVIEW_SKIP_SIGN_IN === '1';
}
