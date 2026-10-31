export interface ScheduleRow {
	questionId: string;
	date: string;
	difficulty: string;
}
export function readPotdEntries(path?: string): { date: string; questionId: string }[];
export function questionDifficulties(): Map<string, string>;
export function scheduleRows(
	entries?: { date: string; questionId: string }[],
	difficulties?: Map<string, string>
): ScheduleRow[];
export function scheduleSql(rows?: ScheduleRow[]): string;
