import { getSupabaseClient } from '$processes/auth/supabase-client';

// Fire-and-forget, same contract as supabase-solved-store.ts: a Supabase
// hiccup here should never block the IDE's Submit flow, only the local
// attempted/solved stores are load-bearing for the student's own session.
export async function recordPotdAttempt(
	questionId: string,
	testsPassed: number,
	testsTotal: number,
	allPassed: boolean
): Promise<void> {
	const supabase = getSupabaseClient();
	const { error } = await supabase.rpc('record_potd_attempt', {
		p_question_id: questionId,
		p_tests_passed: testsPassed,
		p_tests_total: testsTotal,
		p_all_passed: allPassed
	});
	if (error) console.error('Failed to record POTD attempt to Supabase', error);
}
