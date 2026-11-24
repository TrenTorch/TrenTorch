import { describe, it, expect } from 'vitest';
import { aiSystemsParts, domains } from './domains';

describe('domains', () => {
	it('has unique ids', () => {
		expect(new Set(domains.map((d) => d.id)).size).toBe(domains.length);
	});

	it('leaves research papers out of AI Systems', () => {
		expect(aiSystemsParts.length).toBeGreaterThan(0);
		expect(aiSystemsParts.some((part) => part.id === 'part-research-papers')).toBe(false);
	});

	it('lists the live domains before the planned ones', () => {
		const firstPlanned = domains.findIndex((d) => !d.href);
		expect(domains.slice(firstPlanned).every((d) => !d.href)).toBe(true);
	});
});
