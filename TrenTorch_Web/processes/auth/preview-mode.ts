// Preview deployments cannot sign in: Supabase only redirects back to the
// production domain, so every sign-in on a preview URL lands on trentorch.com.
// Preview deployments and local testing can set either flag to bypass sign-in.
// Production does not set them, and signed-out actions stay local.
export function signInSkipped(): boolean {
	return import.meta.env.VITE_PREVIEW_SKIP_SIGN_IN === '1' || import.meta.env.VITE_SIGNUP === '1';
}
