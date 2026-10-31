import { getSupabaseClient } from '$processes/auth/supabase-client';
import { withRpcRetry } from '$processes/supabase/retry-rpc';

export type RecordPotdAttemptResult = { ok: true } | { ok: false; code: string | null };

// A rating update depends on this write landing, so transient failures are
// retried (see withRpcRetry) before the student is told it could not be saved.
export async function recordPotdAttempt(
	questionId: string,
	testsPassed: number,
	testsTotal: number,
	allPassed: boolean
): Promise<RecordPotdAttemptResult> {
	const supabase = getSupabaseClient();
	const { error } = await withRpcRetry(supabase, 'Record POTD attempt', () =>
		supabase.rpc('record_potd_attempt', {
			p_question_id: questionId,
			p_tests_passed: testsPassed,
			p_tests_total: testsTotal,
			p_all_passed: allPassed
		})
	);
	return error ? { ok: false, code: error.code || null } : { ok: true };
}
