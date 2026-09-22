import type { QuestionMetadata } from '$data/curriculum/types';

// potd-rating-system-spec.md's own scale. Deliberately NOT
// data/questions.ts's Easy/Medium/Hard (that one's lossy: Advanced and
// Mastery both collapse to 'Hard' there, see to-display-question.ts's
// DIFFICULTY_MAP) -- rating needs the real four-way split so an Advanced
// and a Mastery POTD don't get treated as equally hard.
export type RatingDifficulty = 'easy' | 'medium' | 'hard' | 'advanced';

// GeneratedQuestion/QuestionMetadata's native scale happens to already be
// four values -- this is a rename, not a collapse.
export const RATING_DIFFICULTY_MAP: Record<QuestionMetadata['difficulty'], RatingDifficulty> = {
	Beginner: 'easy',
	Intermediate: 'medium',
	Advanced: 'hard',
	Mastery: 'advanced'
};

// Difficulty anchors (spec §3) -- the rating at which E == 0.5 exactly for
// that difficulty. Starting placeholders, expected to be retuned once real
// solve-rate data exists; a live rating_event row stores the anchor it
// actually used (see the record_potd_outcome migration) so retuning these
// later doesn't rewrite history.
export const DIFFICULTY_ANCHORS: Record<RatingDifficulty, number> = {
	easy: 550,
	medium: 850,
	hard: 1250,
	advanced: 1850
};

export const STARTING_RATING = 400;
export const RATING_FLOOR = 400;
export const K_GAIN = 100;
export const K_LOSS = 20;

export type PotdOutcome = 'solved' | 'failed';

export interface RatingChange {
	expectedE: number;
	delta: number;
	ratingAfter: number;
}

// E = 1 / (1 + 10^((R_problem - R_user) / 400)) -- spec §2, identical in
// form to Elo's expected-win-probability.
export function expectedSolveProbability(ratingUser: number, ratingProblem: number): number {
	return 1 / (1 + 10 ** ((ratingProblem - ratingUser) / 400));
}

// Pure reimplementation of what supabase/migrations/
// 20260922120003_record_potd_outcome_rpc_and_lock_user_rating.sql's
// record_potd_outcome() does in plpgsql -- that function is the real,
// authoritative write (it also verifies the question/difficulty
// server-side, which this function has no way to do), but its SQL logic
// has to match this line for line. Keeping this pure/TS-only version
// around lets the formula itself be unit-tested directly, and lets the UI
// show a "solving this would earn ~X" preview without a round trip.
export function applyPotdOutcome(
	ratingBefore: number,
	difficulty: RatingDifficulty,
	outcome: PotdOutcome
): RatingChange {
	const anchor = DIFFICULTY_ANCHORS[difficulty];
	const expectedE = expectedSolveProbability(ratingBefore, anchor);

	if (outcome === 'solved') {
		const delta = Math.round(K_GAIN * (1 - expectedE));
		return { expectedE, delta, ratingAfter: ratingBefore + delta };
	}

	// On fail: loss capped by K_LOSS, then the whole thing floored at 400
	// (spec §5.2). delta is recomputed from the clamped result so it always
	// matches the rating's actual movement rather than the pre-floor raw
	// loss.
	const rawLoss = Math.round(K_LOSS * expectedE);
	const ratingAfter = Math.max(RATING_FLOOR, ratingBefore - rawLoss);
	return { expectedE, delta: ratingAfter - ratingBefore, ratingAfter };
}

export interface RatingTier {
	name: string;
	min: number;
	max: number | null;
}

// Tier boundaries and names (spec §6), half-open [min, max) except the top
// tier -- this is the convention the anchors themselves already assume
// (e.g. the Easy anchor 550 is the midpoint of [400, 700)).
export const RATING_TIERS: RatingTier[] = [
	{ name: 'Hello World', min: 400, max: 700 },
	{ name: 'Segfault Survivor', min: 700, max: 1000 },
	{ name: 'Knight of the Kernel', min: 1000, max: 1500 },
	{ name: 'Ace of Attention', min: 1500, max: 1700 },
	{ name: 'Conqueror of CUDA', min: 1700, max: 2000 },
	{ name: 'Singularity', min: 2000, max: null }
];

export function tierForRating(rating: number): RatingTier {
	return (
		RATING_TIERS.find((tier) => rating >= tier.min && (tier.max === null || rating < tier.max)) ??
		RATING_TIERS[0]
	);
}

// §7's 1500 threshold gates a real interview referral, so a single-day
// spike shouldn't be able to fire it -- "stayed at or above 1500 for 7
// consecutive days" is the specific option the spec names as its own
// recommendation (over a rolling average), and it's checkable from
// rating_event history alone (no extra state to keep in sync), so that's
// what this implements. history is every rating_event.rating_after for one
// user, oldest first.
export const INTERVIEW_REFERRAL_THRESHOLD = 1500;
export const INTERVIEW_REFERRAL_STREAK_DAYS = 7;

export function qualifiesForInterviewReferral(ratingAfterHistoryOldestFirst: number[]): boolean {
	if (ratingAfterHistoryOldestFirst.length < INTERVIEW_REFERRAL_STREAK_DAYS) return false;
	const tail = ratingAfterHistoryOldestFirst.slice(-INTERVIEW_REFERRAL_STREAK_DAYS);
	return tail.every((rating) => rating >= INTERVIEW_REFERRAL_THRESHOLD);
}
