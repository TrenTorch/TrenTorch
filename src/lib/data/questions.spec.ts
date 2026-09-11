import { describe, it, expect } from 'vitest';
import { curriculum, getProgressStats } from './questions';

describe('curriculum data', () => {
	it('has seven parts', () => {
		expect(curriculum).toHaveLength(7);
	});

	it('every question has a unique slug', () => {
		const slugs = curriculum.flatMap((part) =>
			part.tracks.flatMap((track) => track.questions.map((q) => q.slug))
		);
		expect(new Set(slugs).size).toBe(slugs.length);
		expect(slugs.length).toBeGreaterThan(100);
	});

	it('every track has at least one question', () => {
		for (const part of curriculum) {
			for (const track of part.tracks) {
				expect(track.questions.length).toBeGreaterThan(0);
			}
		}
	});
});

describe('getProgressStats', () => {
	it('total matches the real question count', () => {
		const stats = getProgressStats();
		const total = curriculum.flatMap((p) => p.tracks.flatMap((t) => t.questions)).length;
		expect(stats.total).toBe(total);
	});

	it('completed is between 0 and total', () => {
		const stats = getProgressStats();
		expect(stats.completed).toBeGreaterThanOrEqual(0);
		expect(stats.completed).toBeLessThanOrEqual(stats.total);
	});
});
