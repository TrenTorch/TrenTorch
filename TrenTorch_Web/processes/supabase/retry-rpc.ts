import type { SupabaseClient } from '@supabase/supabase-js';

export interface RpcError {
	code?: string;
	message?: string;
	status?: number;
}

export type RpcOutcome<T> = { data: T | null; error: null } | { data: null; error: RpcError };

const MAX_TRIES = 3;
const BACKOFF_MS = 600;

// Retry only what a retry can fix: a dropped connection, a gateway 5xx, a JWT
// that expired while the student was reading the problem. PostgREST/Postgres
// rejections (schedule mismatch, check violations, RLS) are deterministic, so
// retrying them only delays the message.
export function isTransientRpcError(error: RpcError): boolean {
	if (error.status !== undefined && error.status >= 500) return true;
	// supabase-js reports fetch failures with status 0 (or none) and no code.
	return (error.status === 0 || error.status === undefined) && !error.code;
}

export function isExpiredSessionError(error: RpcError): boolean {
	return (
		error.status === 401 ||
		error.code === 'PGRST301' ||
		error.code === 'PGRST303' ||
		/jwt expired/i.test(error.message ?? '')
	);
}

const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

export async function withRpcRetry<T>(
	supabase: SupabaseClient,
	label: string,
	call: () => PromiseLike<{ data: T | null; error: RpcError | null; status?: number }>
): Promise<RpcOutcome<T>> {
	let last: RpcError = {};
	for (let attempt = 1; attempt <= MAX_TRIES; attempt++) {
		let error: RpcError | null;
		let data: T | null = null;
		try {
			const res = await call();
			data = res.data;
			error = res.error ? { ...res.error, status: res.status } : null;
		} catch (e) {
			error = { message: e instanceof Error ? e.message : String(e), status: 0 };
		}
		if (!error) return { data, error: null };

		last = error;
		console.error(`${label} failed (try ${attempt}/${MAX_TRIES})`, error);
		if (attempt === MAX_TRIES) break;
		if (isExpiredSessionError(error)) {
			const { error: refreshError } = await supabase.auth.refreshSession();
			if (refreshError) break;
		} else if (!isTransientRpcError(error)) {
			break;
		}
		await sleep(BACKOFF_MS * attempt);
	}
	return { data: null, error: last };
}
