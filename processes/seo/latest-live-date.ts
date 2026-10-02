// A Problem of the Day goes live on the reader's own calendar date, so it is
// already "today" for readers up to UTC+14 while UTC is still on the day
// before. Search visibility follows the earliest timezone, otherwise a build
// run in UTC would keep a live problem out of search for most of its day.
const EARLIEST_TIMEZONE_OFFSET_HOURS = 14;

export function latestLiveDate(now: Date = new Date()): string {
	const shifted = new Date(now.getTime() + EARLIEST_TIMEZONE_OFFSET_HOURS * 60 * 60 * 1000);
	return shifted.toISOString().slice(0, 10);
}
