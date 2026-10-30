import { describe, expect, it } from 'vitest';
import { guideTabsFor } from './guide-tabs';

const potd = [{ questionId: 'potd-q', date: '2026-10-20' }];

describe('guideTabsFor', () => {
	it('gives a DSA question Description, Solution and Discussion, with no Theory tab', () => {
		expect(guideTabsFor({ id: 'sheet-count-pairs', kind: 'dsa' }, [], null)).toEqual([
			'description',
			'solution',
			'discussion'
		]);
	});

	it('shows a DSA question the same tabs whatever the date, so it does not depend on being solved', () => {
		const tabs = ['description', 'solution', 'discussion'];
		expect(guideTabsFor({ id: 'sheet-x', kind: 'dsa' }, potd, '2026-01-01')).toEqual(tabs);
		expect(guideTabsFor({ id: 'sheet-x', kind: 'dsa' }, potd, '2030-01-01')).toEqual(tabs);
	});

	it('does not let a POTD entry for the same id cut a DSA question down', () => {
		const entries = [{ questionId: 'sheet-x', date: '2026-10-20' }];
		expect(guideTabsFor({ id: 'sheet-x', kind: 'dsa' }, entries, '2026-10-20')).toEqual([
			'description',
			'solution',
			'discussion'
		]);
	});

	it('gives the full set before the content has loaded', () => {
		expect(guideTabsFor(undefined, potd, '2026-10-21')).toEqual(['description', 'theory', 'solution']);
	});

	it('gives an ordinary question the full set', () => {
		expect(guideTabsFor({ id: 'plain-q', kind: 'problem' }, potd, '2026-10-21')).toEqual([
			'description',
			'theory',
			'solution'
		]);
	});

	it("keeps a POTD question to Description and Discussion on its own day and before it", () => {
		expect(guideTabsFor({ id: 'potd-q' }, potd, '2026-10-20')).toEqual(['description', 'discussion']);
		expect(guideTabsFor({ id: 'potd-q' }, potd, '2026-10-19')).toEqual(['description', 'discussion']);
	});

	it('brings Theory back for a POTD question once its day has passed, but never Solution', () => {
		expect(guideTabsFor({ id: 'potd-q' }, potd, '2026-10-21')).toEqual([
			'description',
			'theory',
			'discussion'
		]);
	});

	it('gives a POTD question the full set when there is no "today" yet (prerender)', () => {
		expect(guideTabsFor({ id: 'potd-q' }, potd, null)).toEqual(['description', 'theory', 'solution']);
	});
});
