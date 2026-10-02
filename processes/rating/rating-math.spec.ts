import { describe, it, expect } from 'vitest';
import {
	applyPotdOutcome,
	expectedSolveProbability,
	tierForRating,
	qualifiesForInterviewReferral,
	RATING_FLOOR,
	DIFFICULTY_ANCHORS,
	RATING_DIFFICULTY_MAP
} from './rating-math';

// potd-rating-system-spec.md §4's worked-examples table prefixes every E
// value with "~" and is explicitly illustrative, not a computed-and-locked
// oracle -- recomputing it by hand against the anchors §3 actually
// finalizes (Hard = 1250, not the ~1301 the table's own "1000-rated solves
// Hard, E~0.15" line would imply) shows the table's numbers are close but
// not bit-exact to what §2's formula produces from those anchors. These
// tests assert against the exact formula/anchors (the parts of the spec
// marked "finalized"), with a tolerance loose enough to confirm each
// scenario still lands in the same ballpark the spec describes.
describe('expectedSolveProbability (spec §2)', () => {
	it('is 0.5 exactly when user rating equals the problem anchor', () => {
		expect(expectedSolveProbability(850, 850)).toBeCloseTo(0.5, 10);
	});

	it('rises as the user gets stronger relative to the anchor', () => {
		const weak = expectedSolveProbability(400, 1250);
		const strong = expectedSolveProbability(2200, 1250);
		expect(strong).toBeGreaterThan(weak);
	});
});

describe('applyPotdOutcome (spec §4 worked examples, ±tolerance for the table\'s own "~")', () => {
	it('400-rated solves Hard: near-max reward for a huge upset', () => {
		const { expectedE, delta } = applyPotdOutcome(400, 'hard', 'solved');
		expect(expectedE).toBeCloseTo(0.006, 1);
		expect(delta).toBe(99);
	});

	it('1000-rated solves Easy: barely moves', () => {
		const { delta } = applyPotdOutcome(1000, 'easy', 'solved');
		expect(delta).toBeGreaterThan(0);
		expect(delta).toBeLessThanOrEqual(7);
	});

	it('1000-rated solves Hard: solid reward for punching above level', () => {
		const { delta } = applyPotdOutcome(1000, 'hard', 'solved');
		expect(delta).toBeGreaterThan(70);
		expect(delta).toBeLessThan(90);
	});

	it('1000-rated fails Hard: a small loss', () => {
		const { delta } = applyPotdOutcome(1000, 'hard', 'failed');
		expect(delta).toBeLessThan(0);
		expect(delta).toBeGreaterThanOrEqual(-5);
	});

	it('1000-rated fails Medium: stings more than failing Hard, since it was closer to their level', () => {
		const failHard = applyPotdOutcome(1000, 'hard', 'failed');
		const failMedium = applyPotdOutcome(1000, 'medium', 'failed');
		expect(failMedium.delta).toBeLessThan(failHard.delta);
	});

	it('2200-rated solves Easy: essentially nothing, the anti-farming property', () => {
		const { delta } = applyPotdOutcome(2200, 'easy', 'solved');
		expect(delta).toBe(0);
	});
});

describe('rating floor (spec §5.2)', () => {
	it('never drops a rating below 400 even on a near-certain fail', () => {
		const { ratingAfter } = applyPotdOutcome(405, 'advanced', 'failed');
		expect(ratingAfter).toBeGreaterThanOrEqual(RATING_FLOOR);
	});

	it('logs the clamped delta, not the raw pre-floor loss', () => {
		// 'easy' (not 'advanced'): a low-rated user has a HIGH expected E on an
		// easy problem, so that's the difficulty whose raw loss actually
		// reaches the floor here -- failing something far above your level
		// (like 'advanced') has a tiny E and barely costs anything either way.
		const { delta, ratingAfter } = applyPotdOutcome(402, 'easy', 'failed');
		expect(ratingAfter).toBe(RATING_FLOOR);
		expect(delta).toBe(RATING_FLOOR - 402);
	});

	it('is a no-op at exactly the floor', () => {
		const { delta, ratingAfter } = applyPotdOutcome(400, 'advanced', 'failed');
		expect(delta).toBe(0);
		expect(ratingAfter).toBe(400);
	});
});

describe('asymmetry (spec §2: K_gain=100, K_loss=20, 5:1 on purpose)', () => {
	it('a coin-flip solve (E=0.5) gains far more than a coin-flip fail loses', () => {
		const solve = applyPotdOutcome(850, 'medium', 'solved');
		const fail = applyPotdOutcome(850, 'medium', 'failed');
		expect(solve.delta).toBe(50);
		expect(fail.delta).toBe(-10);
	});
});

describe('difficulty anchors and mapping (spec §3)', () => {
	it('every anchor is the midpoint of its tier', () => {
		expect(DIFFICULTY_ANCHORS.easy).toBe(550);
		expect(DIFFICULTY_ANCHORS.medium).toBe(850);
		expect(DIFFICULTY_ANCHORS.hard).toBe(1250);
		expect(DIFFICULTY_ANCHORS.advanced).toBe(1850);
	});

	it('maps the curriculum difficulty scale onto the rating scale 1:1', () => {
		expect(RATING_DIFFICULTY_MAP.Beginner).toBe('easy');
		expect(RATING_DIFFICULTY_MAP.Intermediate).toBe('medium');
		expect(RATING_DIFFICULTY_MAP.Advanced).toBe('hard');
		expect(RATING_DIFFICULTY_MAP.Mastery).toBe('advanced');
	});
});

describe('tierForRating (spec §6)', () => {
	it.each([
		[400, 'Hello World'],
		[699, 'Hello World'],
		[700, 'Segfault Survivor'],
		[999, 'Segfault Survivor'],
		[1000, 'Knight of the Kernel'],
		[1499, 'Knight of the Kernel'],
		[1500, 'Ace of Attention'],
		[1699, 'Ace of Attention'],
		[1700, 'Conqueror of CUDA'],
		[1999, 'Conqueror of CUDA'],
		[2000, 'Singularity'],
		[9999, 'Singularity']
	] as const)('rating %i is %s', (rating, expectedTier) => {
		expect(tierForRating(rating).name).toBe(expectedTier);
	});
});

describe('qualifiesForInterviewReferral (spec §7: hold, not touch, the 1500 threshold)', () => {
	it('does not fire on a single spike above 1500', () => {
		expect(qualifiesForInterviewReferral([1000, 1200, 1600])).toBe(false);
	});

	it('does not fire on fewer than 7 days of history at all', () => {
		expect(qualifiesForInterviewReferral([1600, 1600, 1600])).toBe(false);
	});

	it('does not fire if the streak dips below 1500 partway through', () => {
		expect(qualifiesForInterviewReferral([1600, 1600, 1400, 1600, 1600, 1600, 1600])).toBe(false);
	});

	it('fires after 7 consecutive days at or above 1500', () => {
		expect(qualifiesForInterviewReferral([1000, 1600, 1600, 1600, 1600, 1600, 1600, 1600])).toBe(
			true
		);
	});

	it('fires at exactly the threshold, not only strictly above it', () => {
		expect(qualifiesForInterviewReferral(new Array(7).fill(1500))).toBe(true);
	});
});
