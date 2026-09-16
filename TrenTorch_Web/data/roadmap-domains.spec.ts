import { describe, it, expect } from 'vitest';
import { curriculum } from './questions';
import { domainDefs, SKIP_ELIGIBLE_PART_ID } from './roadmap-domains';

describe('roadmap domains', () => {
	const realPartIds = new Set(curriculum.map((p) => p.id));

	it('every domain references at least one real Part id', () => {
		for (const domain of domainDefs) {
			expect(domain.partIds.length).toBeGreaterThan(0);
			for (const partId of domain.partIds) {
				expect(realPartIds.has(partId)).toBe(true);
			}
		}
	});

	it('domain ids are unique', () => {
		const ids = domainDefs.map((d) => d.id);
		expect(new Set(ids).size).toBe(ids.length);
	});

	it('the skip-eligible part exists in the curriculum', () => {
		expect(realPartIds.has(SKIP_ELIGIBLE_PART_ID)).toBe(true);
	});
});
