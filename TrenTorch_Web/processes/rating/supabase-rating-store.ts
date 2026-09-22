import { getSupabaseClient } from '$processes/auth/supabase-client';
import type { PotdOutcome } from './rating-math';

export interface RecordPotdOutcomeResult {
	ratingAfter: number;
	delta: number;
	alreadyRecorded: boolean;
}

// The only client-side entry point into record_potd_outcome() (see
// supabase/migrations/20260922120003_record_potd_outcome_rpc_and_lock_user_rating.sql).
// Deliberately takes just (questionId, outcome) -- no difficulty, no
// rating, no delta -- because the RPC looks difficulty up itself from
// potd_schedule and computes the delta itself; nothing here could be
// trusted if it were client-supplied anyway.
export async function recordPotdOutcome(
	questionId: string,
	outcome: PotdOutcome
): Promise<RecordPotdOutcomeResult | null> {
	const supabase = getSupabaseClient();
	const { data, error } = await supabase
		.rpc('record_potd_outcome', { p_question_id: questionId, p_outcome: outcome })
		.single<{ rating_after: number; delta: number; already_recorded: boolean }>();
	if (error) {
		console.error('Failed to record POTD rating outcome', error);
		return null;
	}
	return {
		ratingAfter: data.rating_after,
		delta: data.delta,
		alreadyRecorded: data.already_recorded
	};
}

// Server-side twin of attempted.svelte.ts's local set (see potd_attempts's
// migration for why this needs to be durable/cross-device). Fire-and-forget
// like every other Supabase write in this codebase -- a failure here just
// means the day-end settlement check has nothing to settle later, which is
// no worse than the user never having attempted it.
export async function recordPotdAttempt(userId: string, questionId: string): Promise<void> {
	const supabase = getSupabaseClient();
	const { error } = await supabase
		.from('potd_attempts')
		.upsert({ user_id: userId, question_id: questionId }, { onConflict: 'user_id,question_id' });
	if (error) console.error('Failed to record POTD attempt', error);
}

export async function fetchUnratedPastAttempts(userId: string): Promise<string[]> {
	const supabase = getSupabaseClient();
	const { data: attempts, error: attemptsError } = await supabase
		.from('potd_attempts')
		.select('question_id')
		.eq('user_id', userId);
	if (attemptsError) {
		console.error('Failed to fetch POTD attempts', attemptsError);
		return [];
	}
	if (!attempts || attempts.length === 0) return [];

	const { data: rated, error: ratedError } = await supabase
		.from('rating_event')
		.select('question_id')
		.eq('user_id', userId);
	if (ratedError) {
		console.error('Failed to fetch rating events', ratedError);
		return [];
	}
	const ratedIds = new Set((rated ?? []).map((row) => row.question_id));
	return attempts.map((row) => row.question_id).filter((id) => !ratedIds.has(id));
}
