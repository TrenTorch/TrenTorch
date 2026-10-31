import { getSupabaseClient } from '$processes/auth/supabase-client';

export type RecordPotdAttemptResult = { ok: true } | { ok: false; code: string | null };

const MAX_ATTEMPTS = 3;
const BACKOFF_MS = 600;

interface RpcError {
	code?: string;
	message?: string;
	status?: number;
}

// A rating update depends on this write landing, so a one-off blip (dropped
// connection, gateway 5xx, a JWT that expired while the student was reading
// the problem) must not surface as a failed save. Postgres/PostgREST rejections
// (schedule mismatch, check violations, RLS) are deterministic: retrying them
// only delays the message.
export function isTransientRpcError(error: RpcError): boolean {
	if (error.status !== undefined && error.status >= 500) return true;
	if (error.status === 0 || error.status === undefined) {
		// supabase-js reports fetch failures with no HTTP status and no code.
		return !error.code;
	}
	return false;
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

export async function recordPotdAttempt(
	questionId: string,
	testsPassed: number,
	testsTotal: number,
	allPassed: boolean
): Promise<RecordPotdAttemptResult> {
	const supabase = getSupabaseClient();
	let lastCode: string | null = null;

	for (let attempt = 1; attempt <= MAX_ATTEMPTS; attempt++) {
		let error: RpcError | null;
		try {
			const res = await supabase.rpc('record_potd_attempt', {
				p_question_id: questionId,
				p_tests_passed: testsPassed,
				p_tests_total: testsTotal,
				p_all_passed: allPassed
			});
			error = res.error ? { ...res.error, status: res.status } : null;
		} catch (e) {
			error = { message: e instanceof Error ? e.message : String(e), status: 0 };
		}
		if (!error) return { ok: true };

		lastCode = error.code || null;
		console.error(
			`Failed to record POTD attempt to Supabase (try ${attempt}/${MAX_ATTEMPTS})`,
			error
		);

		if (attempt === MAX_ATTEMPTS) break;
		if (isExpiredSessionError(error)) {
			const { error: refreshError } = await supabase.auth.refreshSession();
			if (refreshError) break;
		} else if (!isTransientRpcError(error)) {
			break;
		}
		await sleep(BACKOFF_MS * attempt);
	}
	return { ok: false, code: lastCode };
}
