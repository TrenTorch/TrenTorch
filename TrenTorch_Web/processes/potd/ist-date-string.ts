// IST (Asia/Kolkata, UTC+5:30) has no daylight saving, so a fixed offset is
// exact. This is the single canonical day boundary for POTD: which problem
// is served as "today's", whether a solve counts as current for rating, and
// when the countdown rolls over. All three must agree, or a visitor can see
// one day's problem while the rating check silently uses another.
const IST_OFFSET_MS = 5.5 * 60 * 60 * 1000;

export function istDateString(date: Date): string {
	const shifted = new Date(date.getTime() + IST_OFFSET_MS);
	return shifted.toISOString().slice(0, 10);
}

/** The next IST midnight after `date`, when the POTD rotates, as a real UTC instant. */
export function nextPotdRollover(date: Date): Date {
	const shifted = new Date(date.getTime() + IST_OFFSET_MS);
	const nextShiftedMidnight = Date.UTC(
		shifted.getUTCFullYear(),
		shifted.getUTCMonth(),
		shifted.getUTCDate() + 1
	);
	return new Date(nextShiftedMidnight - IST_OFFSET_MS);
}
