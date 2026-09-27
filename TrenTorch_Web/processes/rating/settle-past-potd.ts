import { potdEntries } from '$data/potd';
import { localDateString } from '$processes/potd/local-date-string';
import { fetchUnratedPastAttempts, recordPotdOutcome } from './supabase-rating-store';

// Spec §5.1: the "failed" rating event only fires once a POTD's day has
// fully passed, never on the first failed Submit (a student should be free
// to keep debugging the same day without being penalized). This app has no
// server/cron of its own (every page is prerendered static, see
// platform/routes/ide/[id]/+page.ts's own comment on that), so there is no
// midnight trigger -- this lazily settles any past-due, still-unrated
// attempt the next time the signed-in student's client runs it. A student
// who never comes back after failing simply never gets the loss applied,
// which matches §5.4's own philosophy: rating isn't an attendance penalty,
// so there's no urgency to chase it down.
//
// record_potd_outcome() is idempotent per (user, question_id), so calling
// this on every app load is safe -- an already-solved or already-settled
// question is a no-op.
export async function settlePastPotdOutcomes(userId: string): Promise<void> {
	const today = localDateString(new Date());
	const unrated = await fetchUnratedPastAttempts(userId);
	if (unrated.length === 0) return;

	for (const questionId of unrated) {
		const entry = potdEntries.find((e) => e.questionId === questionId);
		// Not a real POTD entry, or still today/future: nothing to settle yet.
		if (!entry || entry.date >= today) continue;
		await recordPotdOutcome(questionId, 'failed');
	}
}
